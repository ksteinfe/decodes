using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Parameters;
using Grasshopper.Kernel.Parameters.Hints;
using System.Windows.Forms;
using System.Text.RegularExpressions;

namespace DcPython.Decodes
{
    class Decodes_Param_ScriptVariable : Param_ScriptVariable
    {
        new public bool AllowTreeAccess = false;
        new public bool IsBakeCapable = false;
        new public bool IsPreviewCapable = false;

        public Decodes_Param_ScriptVariable() : base() { }
        

        public Decodes_Param_ScriptVariable(Param_ScriptVariable other)
        {
            this.CopyFrom(other);
            this.Access = other.Access;
            this.DataMapping = other.DataMapping;
            this.Optional = other.Optional;
            this.Reverse = other.Reverse;
            this.Simplify = other.Simplify;
            this.WireDisplay = other.WireDisplay;

            this.TypeHint = other.TypeHint;
            this.Hints = other.Hints;
            this.ShowHints = other.ShowHints;

            this.Name = other.Name;
            this.NickName = other.NickName;

            

            FixGhInput();
        }

        public override bool AppendMenuItems(ToolStripDropDown menu)
        {
            Menu_AppendTextItem(menu, this.NickName.Replace("[","").Replace("]",""), new Grasshopper.GUI.GH_MenuTextBox.KeyDownEventHandler(Menu_NameKeyDown), new Grasshopper.GUI.GH_MenuTextBox.TextChangedEventHandler(Menu_NameTextChanged), true);
            base.AppendAdditionalMenuItems(menu);
            //Menu_AppendObjectName(menu);
            //Menu_AppendWireDisplay(menu);
            //Menu_AppendDisconnectWires(menu);
            //Menu_AppendSeparator(menu);
            //Menu_AppendItem(menu, "List", Menu_ListAccessClicked, true, this.Access == GH_ParamAccess.list);
            return true;
        }

        private void Menu_NameKeyDown(Object sender, EventArgs e)  { }
        private void Menu_NameTextChanged(Object sender, string text)
        {
            this.NickName = text;
            FixGhInput();
            this.OnAttributesChanged();
            this.OnDisplayExpired(true);
            this.ExpireSolution(true);
        }

        public void FixGhInput()
        {
            NickName = cleanNickname(NickName);
            NickName = NickName.Replace("_" + Decodes_PythonComponent.attributes_suffix, "_baduser");
            if (String.Compare(NickName, "code", StringComparison.InvariantCultureIgnoreCase) == 0) NickName = "baduser";
            
            Name = NickName; // set name to nickname, omitting array brackets (added below)

            if (Access == GH_ParamAccess.list) NickName = "[" + NickName + "]";

            if (string.IsNullOrEmpty(Description)) Description = string.Format("Script variable {0}", Name);
            Optional = true;
            ShowHints = true;

            Hints = Decodes_PythonComponent.GetHints();
            if (TypeHint == null) TypeHint = Hints[0];
        }

        public static string cleanNickname(string str)
        {
            str = Regex.Replace(str, @"\s+", " "); // collapse multiple spaces
            str = str.Trim().Replace(" ", "_");
            str = Regex.Replace(str, @"[^\w\.@:-]", ""); // only allow normal word chars, dashes, underbars
            return str;
        }


    }
}
