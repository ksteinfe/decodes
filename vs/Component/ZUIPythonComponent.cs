using System.Linq;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Parameters;
using Grasshopper.Kernel.Parameters.Hints;
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;

namespace GhPython.Component
{
  [Guid("4CC91116-E9CC-46E7-8ABB-9671F0B72594")]
  public class ZuiPythonComponent : ScriptingAncestorComponent, IGH_VariableParameterComponent
  {
      //ksteinfe
      List<string> used_script_variable_names;
      List<string> script_variables_in_use;
      string attributes_suffix = "prop";
    
      public ZuiPythonComponent()
    {
      CodeInputVisible = false;
      Params.ParameterChanged += ParameterChanged;
    }

      protected override void AddDefaultInput(GH_Component.GH_InputParamManager pManager)
      {
          pManager.RegisterParam(CreateParameter(GH_ParameterSide.Input, pManager.ParamCount));
          pManager.RegisterParam(CreateParameter(GH_ParameterSide.Input, pManager.ParamCount));
      }

      protected override void AddDefaultOutput(GH_Component.GH_OutputParamManager pManager)
      {
          pManager.RegisterParam(CreateParameter(GH_ParameterSide.Output, pManager.ParamCount));
      }


    internal override void FixGhInput(Param_ScriptVariable i, bool alsoSetIfNecessary = true)
    {
      i.Name = i.NickName;

      if (string.IsNullOrEmpty(i.Description))
        i.Description = string.Format("Script variable {0}", i.NickName);
      i.AllowTreeAccess = true;
      i.Optional = true;
      i.ShowHints = true;
      i.Hints = GetHints();

      if (alsoSetIfNecessary && i.TypeHint == null)
        i.TypeHint = i.Hints[0]; // ksteinfe: it looks like this is where the default hint is set
    }

    static readonly List<IGH_TypeHint> m_hints = new List<IGH_TypeHint>();
    static List<IGH_TypeHint> GetHints()
    {
      lock (m_hints)
      {
        if (m_hints.Count == 0)
        {
          m_hints.Add(new NoChangeHint());
          //m_hints.Add(new GhDocGuidHint()); ksteinfe removed

          m_hints.AddRange(PossibleHints);

          m_hints.RemoveAll(t =>
            {
              var y = t.GetType();
              return (y == typeof (GH_DoubleHint_CS) || y == typeof (GH_StringHint_CS));
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
    


    public IGH_Param CreateInputParam(GH_ParameterSide side, int index)
    {
        return new Param_ScriptVariable
        {
            NickName = GH_ComponentParamServer.InventUniqueNickname("xyzuvwst", this.Params.Input),
            Name = NickName,
            Description = "Script variable " + NickName,
        };
    }


    public IGH_Param CreateParameter(GH_ParameterSide side, int index) { return CreateParameter(side, index, false); }
    public IGH_Param CreateParameter(GH_ParameterSide side, int index, bool is_twin)
    {
        switch (side)
        {
            case GH_ParameterSide.Input: return CreateInputParam(side, index);
            case GH_ParameterSide.Output:
                IGH_Param p;
                if (!is_twin)
                {
                    if (used_script_variable_names == null)
                    {
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
                }
                else
                {
                    if (Params.Output.Count <= 1) return null;
                    string nickname = AttNicknameFromGeomNickname(Params.Output[index - 1].NickName);
                    Param_String prop = new Param_String();
                    prop.NickName = nickname;
                    prop.Name = nickname;
                    prop.Description = "Contains the non-geometric properties of the geometry found in the parameter above";
                    prop.MutableNickName = false;
                    p = prop;
                }
                return p;
            default:
                {
                    return null;
                }
        }
    }

    public bool NicknameSuggestsGeometryOutputParam(IGH_Param param)
    {
        try { return ((Params.IndexOfOutputParam(param.Name)!=0)&&(!param.NickName.Contains("_"+attributes_suffix))); }
        catch { return false; }
    }
    public bool NicknameSuggestsAttributesOutputParam(IGH_Param param)
    {
        try { return (param.NickName.Contains("_" + attributes_suffix)); }
        catch { return false; }
    }

    public string AttNicknameFromGeomNickname(string nickname){
        return nickname.Trim().Replace(' ', '_') + "_" + attributes_suffix;
    }


      void ParameterChanged(object sender, GH_ParamServerEventArgs e) { VariableParameterMaintenance();    }

    bool IGH_VariableParameterComponent.DestroyParameter(GH_ParameterSide side, int index)
    {
        if  ((side == GH_ParameterSide.Output)&&(NicknameSuggestsGeometryOutputParam(Params.Output[index])))
        {
            Params.UnregisterOutputParameter(Params.Output[index + 1]);
        }
      return true;
    }

    bool IGH_VariableParameterComponent.CanInsertParameter(GH_ParameterSide side, int index)
    {
      if (side == GH_ParameterSide.Input)
        return index > (!CodeInputVisible ? -1 : 0);
      if (side == GH_ParameterSide.Output)
      {
          if (index == 0) return false;
          if (!NicknameSuggestsGeometryOutputParam(Params.Output[index-1])) return true;
          return false;
      }
      return false;
    }

    bool IGH_VariableParameterComponent.CanRemoveParameter(GH_ParameterSide side, int index)
    {
        if (side == GH_ParameterSide.Input) return true;
        if (index==0) return false;
        if (NicknameSuggestsGeometryOutputParam(Params.Output[index])) return true;
        return false;
    }

    public override void VariableParameterMaintenance()
    {
      foreach (Param_ScriptVariable variable in Params.Input.OfType<Param_ScriptVariable>())
        FixGhInput(variable);

      foreach (Param_GenericObject i in Params.Output.OfType<Param_GenericObject>())
      {
        i.NickName = i.NickName.Replace("_" + attributes_suffix, "_baduser");
        i.NickName = i.NickName.Trim().Replace(" ","_");
        i.Name = i.NickName;
        i.Description = "Contains the translated geometry found in outie " + i.NickName;
      }

      foreach (Param_GenericObject i in Params.Input)
      {
          i.NickName = i.NickName.Replace("_" + attributes_suffix, "_baduser");
          i.NickName = i.NickName.Trim().Replace(" ", "_");
          i.Name = i.NickName;
      }

      for (int i = 1; i < Params.Output.Count; i++)
      {
          if (NicknameSuggestsGeometryOutputParam(Params.Output[i]))
          {
              if ((i == Params.Output.Count - 1) || (!NicknameSuggestsAttributesOutputParam(Params.Output[i + 1])))
              {
                  Params.RegisterOutputParam(CreateParameter(GH_ParameterSide.Output, i + 1, true), i + 1);
              }
              else if (Params.Output[i+1].NickName != AttNicknameFromGeomNickname(Params.Output[i].NickName))
              {
                  Params.Output[i+1].NickName = AttNicknameFromGeomNickname(Params.Output[i].NickName);
                  Params.Output[i + 1].Name = AttNicknameFromGeomNickname(Params.Output[i].NickName);
              }
              
          }
      }


    }


    protected override void SetScriptTransientGlobals()
    {
      base.SetScriptTransientGlobals();

      _py.ScriptContextDoc = _document;
      _marshal = new NewComponentIOMarshal(_document, this);
      _py.SetVariable(DOCUMENT_NAME, _document);
      _py.SetIntellisenseVariable(DOCUMENT_NAME, _document);
    }

    public override Guid ComponentGuid
    {
      get { return typeof(ZuiPythonComponent).GUID; }
    }


  }
}
