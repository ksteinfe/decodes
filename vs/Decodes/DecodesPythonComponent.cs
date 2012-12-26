using DcPython.Properties;
using GhPython.Component;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Attributes;
using Grasshopper.Kernel.Parameters;
using Grasshopper.Kernel.Parameters.Hints;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text.RegularExpressions;
using System.Windows.Forms;

namespace DcPython.Decodes {
    [Guid("FCCAD19E-DCB6-44AB-8EDB-54DD6AB7E966")]
    public class Decodes_PythonComponent : ScriptingAncestorComponent, IGH_VariableParameterComponent {

        List<string> used_script_variable_names;
        List<string> script_variables_in_use;
        public static string attributes_suffix = "props";
        bool props_visible;

        public Decodes_PythonComponent() {
            CodeInputVisible = false;
            props_visible = false;
            Params.ParameterChanged += ParameterChanged;

            // fix console name
            Params.Output[0].Name = "console";
            Params.Output[0].NickName = "...";
        }

        #region DYNAMIC VARIABLE STUFF

        protected override void AddDefaultInput( GH_Component.GH_InputParamManager pManager ) {
            pManager.RegisterParam(CreateParameter(GH_ParameterSide.Input, pManager.ParamCount));
        }

        protected override void AddDefaultOutput( GH_Component.GH_OutputParamManager pManager ) {
            pManager.RegisterParam(CreateParameter(GH_ParameterSide.Output, pManager.ParamCount));
        }


        internal override void FixGhInput(Param_ScriptVariable param, bool alsoSetIfNecessary = true) {
            param.NickName = cleanNickname(param.NickName);
            param.NickName = param.NickName.Replace("_" + Decodes_PythonComponent.attributes_suffix, "_baduser");
            if (String.Compare(param.NickName, "code", StringComparison.InvariantCultureIgnoreCase) == 0) param.NickName = "baduser";

            param.Name = param.NickName; // set name to nickname, omitting array brackets (added below)

            //if (param.Access == GH_ParamAccess.list) NickName = "[" + NickName + "]";

            if (string.IsNullOrEmpty(Description)) Description = string.Format("Script variable {0}", Name);
            param.Optional = true;
            param.ShowHints = true;

            param.Hints = Decodes_PythonComponent.GetHints();
            if (param.TypeHint == null) param.TypeHint = param.Hints[0];
        }

        public string cleanNickname(string str)
        {
            str = Regex.Replace(str, @"\s+", " "); // collapse multiple spaces
            str = str.Trim().Replace(" ", "_");
            str = Regex.Replace(str, @"[^\w\.@:-]", ""); // only allow normal word chars, dashes, underbars
            return str;
        }


        static readonly List<IGH_TypeHint> m_hints = new List<IGH_TypeHint>();
        public static List<IGH_TypeHint> GetHints() {
            lock (m_hints) {
                if (m_hints.Count == 0) {
                    m_hints.Add(new NoChangeHint());
                    //m_hints.Add(new GhDocGuidHint()); ksteinfe removed

                    m_hints.AddRange(PossibleHints);

                    m_hints.RemoveAll(t => {
                        var y = t.GetType();
                        return (y == typeof(GH_DoubleHint_CS) || y == typeof(GH_StringHint_CS));
                    });
                    m_hints.Insert(4, new NewFloatHint());
                    m_hints.Insert(6, new NewStrHint());

                    m_hints.Add(new GH_BoxHint());

                    m_hints.Add(new GH_HintSeparator());

                    m_hints.Add(new GH_LineHint());
                    m_hints.Add(new GH_CircleHint());
                    m_hints.Add(new GH_ArcHint());
                    m_hints.Add(new GH_PolylineHint());

                    m_hints.Add(new GH_HintSeparator());

                    m_hints.Add(new GH_CurveHint());
                    m_hints.Add(new GH_MeshHint());
                    m_hints.Add(new GH_SurfaceHint());
                    m_hints.Add(new GH_BrepHint());
                    m_hints.Add(new GH_GeometryBaseHint());
                }
            }
            return m_hints;
        }


        public IGH_Param CreateParameter( GH_ParameterSide side, int index ) { return CreateParameter(side, index, false); }
        public IGH_Param CreateParameter( GH_ParameterSide side, int index, bool is_twin ) {
            switch (side) {
                case GH_ParameterSide.Input:
                    return new Param_ScriptVariable
                    {
                        NickName = GH_ComponentParamServer.InventUniqueNickname("xyzuvwst", this.Params.Input),
                        Name = NickName,
                        Description = "Script variable " + NickName,
                        Access = GH_ParamAccess.item,
                        AllowTreeAccess = false,
                    };
                case GH_ParameterSide.Output:
                    IGH_Param p;
                    if (!is_twin) {
                        if (used_script_variable_names == null) {
                            used_script_variable_names = new List<string>();
                            script_variables_in_use = new List<string>();
                        }
                        string script_variable = GH_ComponentParamServer.InventUniqueNickname("abcdefghijklmn", used_script_variable_names);
                        used_script_variable_names.Add(script_variable);

                        Param_GenericObject geom = new Param_GenericObject();
                        geom.NickName = script_variable;
                        geom.Name = NickName;
                        geom.Description = "Contains the translated geometry found in outie " + script_variable;
                        p = geom;
                    } else {
                        if (Params.Output.Count <= 1) return null;
                        string nickname = AttNicknameFromGeomNickname(Params.Output[index - 1].NickName);
                        //Param_String prop = new Param_String();
                        GHParam_Decodes_Attributes prop = new GHParam_Decodes_Attributes();
                        prop.NickName = nickname;
                        prop.Name = nickname;
                        prop.Description = "Contains the non-geometric properties of the geometry found in the parameter above";
                        prop.MutableNickName = false;
                        p = prop;
                    }
                    return p;
                default: {
                        return null;
                    }
            }
        }

        public bool NicknameSuggestsGeometryOutputParam( IGH_Param param ) {
            try { return ((Params.IndexOfOutputParam(param.Name) != 0) && (!param.NickName.Contains("_" + attributes_suffix))); } catch { return false; }
        }
        public bool NicknameSuggestsAttributesOutputParam( IGH_Param param ) {
            try { return (param.NickName.Contains("_" + attributes_suffix)); } catch { return false; }
        }
        public string AttNicknameFromGeomNickname( string nickname ) {
            return nickname.Trim().Replace(' ', '_') + "_" + attributes_suffix;
        }


        void ParameterChanged( object sender, GH_ParamServerEventArgs e ) { VariableParameterMaintenance(); }

        bool IGH_VariableParameterComponent.DestroyParameter( GH_ParameterSide side, int index ) {
            if ((side == GH_ParameterSide.Output) && (NicknameSuggestsGeometryOutputParam(Params.Output[index])) && (props_visible) ) {
                Params.UnregisterOutputParameter(Params.Output[index + 1]);
            }
            return true;
        }

        bool IGH_VariableParameterComponent.CanInsertParameter( GH_ParameterSide side, int index ) {
            if (side == GH_ParameterSide.Input) return index > (!CodeInputVisible ? -1 : 0);
            if (side == GH_ParameterSide.Output) {
                if (index == 0) return false;
                if (!props_visible) return true;
                if (!NicknameSuggestsGeometryOutputParam(Params.Output[index - 1])) return true;
                return false;
            }
            return false;
        }

        bool IGH_VariableParameterComponent.CanRemoveParameter( GH_ParameterSide side, int index ) {
            if (side == GH_ParameterSide.Input) return true;
            if (index == 0) return false;
            if (NicknameSuggestsGeometryOutputParam(Params.Output[index])) return true;
            return false;
        }

        public override void VariableParameterMaintenance() {
            foreach (Param_ScriptVariable variable in Params.Input.OfType<Param_ScriptVariable>())
                FixGhInput(variable);
            
            // fix names of outputs carrying decodes geometry
            foreach (Param_GenericObject i in Params.Output.OfType<Param_GenericObject>()) {
                i.NickName = i.NickName.Replace("_" + attributes_suffix, "_baduser");
                i.NickName = i.NickName.Trim().Replace(" ", "_");
                i.Name = i.NickName;
                i.Description = "Contains the translated geometry found in outie " + i.NickName;
            }

            // tidy up outputs carrying props
            if (props_visible) {
                bool added_param = false;
                for (int i = 1; i < Params.Output.Count; i++) {
                    if (NicknameSuggestsGeometryOutputParam(Params.Output[i])) {
                        if ((i == Params.Output.Count - 1) || (!NicknameSuggestsAttributesOutputParam(Params.Output[i + 1]))) {
                            Params.RegisterOutputParam(CreateParameter(GH_ParameterSide.Output, i + 1, true), i + 1);
                            added_param = true;
                        } else if (Params.Output[i + 1].NickName != AttNicknameFromGeomNickname(Params.Output[i].NickName)) {
                            Params.Output[i + 1].NickName = AttNicknameFromGeomNickname(Params.Output[i].NickName);
                            Params.Output[i + 1].Name = AttNicknameFromGeomNickname(Params.Output[i].NickName);
                        }
                    }
                }
                if (added_param) {
                    Params.OnParametersChanged();
                    OnDisplayExpired(true);
                    ExpireSolution(true);
                }
            } else {
                if (RemoveAttributeOutputParams(false)) {
                    Params.OnParametersChanged();
                    OnDisplayExpired(true);
                }
            }
        }

        private bool RemoveAttributeOutputParams(bool params_changed) {
            bool all_clean = true;
            foreach (GHParam_Decodes_Attributes param in Params.Output.OfType<GHParam_Decodes_Attributes>())
                if (NicknameSuggestsAttributesOutputParam(param)) {
                    Params.UnregisterParameter(param);
                    all_clean = false;
                    params_changed = true;
                    break;
                }
            if (!all_clean) return RemoveAttributeOutputParams(params_changed);
            return params_changed;
        }
        #endregion


        protected override void SetScriptTransientGlobals() {
            base.SetScriptTransientGlobals();

            _py.ScriptContextDoc = _document;
            _marshal = new NewComponentIOMarshal(_document, this);
            _py.SetVariable(DOCUMENT_NAME, _document);
            _py.SetIntellisenseVariable(DOCUMENT_NAME, _document);
        }


        #region COSMETICS AND GUI STUFF


        public void Menu_OpenEditorClicked( Object sender, EventArgs e ) {
            var attr = Attributes as PythonComponentAttributes;
            if (attr != null) attr.OpenEditor();
        }

        public void Menu_TogglePropsVisibility( Object sender, EventArgs e ) {
            props_visible = !props_visible;
            VariableParameterMaintenance();
        }

        public override bool AppendMenuItems( ToolStripDropDown menu ) {
            Menu_AppendObjectName(menu);
            Menu_AppendPreviewItem(menu);
            Menu_AppendEnableItem(menu);
            Menu_AppendBakeItem(menu);

            Menu_AppendSeparator(menu);

            try {
                Menu_AppendItem(menu, "Open Decodes Editor", Menu_OpenEditorClicked, !Locked);
                menu.Items[5].Font = new Font(menu.Items[5].Font, FontStyle.Bold);
            } catch (Exception ex) { GhPython.Forms.PythonScriptForm.LastHandleException(ex); }
            Menu_AppendItem(menu, "Display Output Properties", Menu_TogglePropsVisibility, true, props_visible);

            Menu_AppendSeparator(menu);

            Menu_AppendWarningsAndErrors(menu);
            Menu_AppendObjectHelp(menu);
            return true;
        }

        protected override string HtmlHelp_Source() {
            return base.HtmlHelp_Source().Replace("\nPython Script", "\n" + NickName);
        }

        protected override string HelpDescription {
            get {
                if (_inDocStringsMode) {
                    if (SpecialPythonHelpContent == null)
                        return base.HelpDescription;
                    return base.HelpDescription +
                           "<br><br>\n<small>Remarks: <i>" +
                           DocStringUtils.Htmlify(SpecialPythonHelpContent) +
                           "</i></small>";
                }
                return Resources.helpText;
            }
        }


        protected override Bitmap Icon { get { return Resources.python; } }


        #endregion


        public override bool Write( GH_IO.Serialization.GH_IWriter writer ) {
            for (int s = 0; s < this.script_variables_in_use.Count; s++ ) writer.SetString("script_variables_in_use["+s+"]", this.script_variables_in_use[s]);
            writer.SetBoolean("props_visible", this.props_visible);
            return base.Write(writer);
        }
        public override bool Read( GH_IO.Serialization.GH_IReader reader ) {
            props_visible = false;
            reader.TryGetBoolean("props_visible", ref props_visible);
            if (props_visible) { VariableParameterMaintenance(); }

            script_variables_in_use = new List<string>();
            for (int s = 0; s < reader.ItemCount; s++) {
                string str = null;
                reader.TryGetString("script_variables_in_use[" + s + "]", ref str);
                if (str != null) script_variables_in_use.Add(str);
            }

            bool ret = base.Read(reader);

            return ret;
        }

        public override Guid ComponentGuid { get { return typeof(Decodes_PythonComponent).GUID; } }
        //public override void CreateAttributes() { m_attributes = new Decodes_PythonComponent_Attributes(this); }

    }




    public class Decodes_PythonComponent_Attributes : GH_ComponentAttributes
    {
        public Decodes_PythonComponent_Attributes(Decodes_PythonComponent owner) : base(owner) { }

        SizeF min_param_size = new SizeF(40, 30);

        protected override void Layout()
        {
            base.Layout();

            // Compute the width of the NickName of each input (plus some extra padding), 
            // then make sure we have at least 80 pixels.
            //int max_width = (int) Math.Ceiling(Owner.Params.InputWidth + Owner.Params.OutputWidth);
            //SizeF input_param_size = min_param_size;
            //SizeF output_param_size = min_param_size;
            //foreach (IGH_Param param in Owner.Params.Input) input_param_size.Width = Math.Max(input_param_size.Width, GH_FontServer.StringWidth(param.NickName, GH_FontServer.Standard));
            //foreach (IGH_Param param in Owner.Params.Output) output_param_size.Width = Math.Max(output_param_size.Width, GH_FontServer.StringWidth(param.NickName, GH_FontServer.Standard));

            //int width = (int) (input_param_size.Width + output_param_size.Width) + 80;
            //int height = Math.Max(Owner.Params.Input.Count, Owner.Params.Output.Count) * ((int) min_param_size.Height);

            // Assign the width and height to the Bounds property.
            // Also, make sure the Bounds are anchored to the Pivot
            //Bounds = new RectangleF(Pivot, new SizeF(width, height));

            //Owner.Params.Input[0].Attributes.Bounds = new RectangleF(new PointF(Bounds.Left, Bounds.Top), input_param_size);
            //Owner.Params.Output[0].Attributes.Bounds = new RectangleF(new PointF(Bounds.Right-output_param_size.Width, Bounds.Top), output_param_size);
            //Owner.Params.Output[1].Attributes.Bounds = new RectangleF(new PointF(Bounds.Right - output_param_size.Width, Bounds.Top+output_param_size.Height), output_param_size);
            
            
        }


    }
}
