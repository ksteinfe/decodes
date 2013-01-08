using System;
using Grasshopper.Kernel.Parameters;
using Grasshopper.Kernel.Parameters.Hints;
using Rhino.Geometry;
using System.Collections.Generic;
using System.Runtime.InteropServices;

namespace GhPython.Component
{
  [Guid("39FBC626-7A01-46AB-A18E-EC1C0C41685B")]
  public class NewFloatHint : GH_DoubleHint_CS, IGH_TypeHint
  {
    Guid IGH_TypeHint.HintID { get { return this.GetType().GUID; } }

    string IGH_TypeHint.TypeName { get { return "float"; } }
  }

  [Guid("37261734-EEC7-4F50-B6A8-B8D1F3C4396B")]
  public class NewStrHint : GH_StringHint_CS, IGH_TypeHint
  {
    Guid IGH_TypeHint.HintID { get { return this.GetType().GUID; } }

    string IGH_TypeHint.TypeName { get { return "str"; } }
  }


    /*
  [Guid("87F87F55-5B71-41F4-8AEA-21D494016F81")]
  public class GhDocGuidHint : GH_NullHint, IGH_TypeHint
  {
    Guid IGH_TypeHint.HintID { get { return this.GetType().GUID; } }
//ksteinfe it looks like this is casting from GH objects to Rhinocommon objects?
    bool IGH_TypeHint.Cast(object data, out object target)
    {
      bool toReturn = base.Cast(data, out target);

      if (toReturn && target != null)
      {
        Type t = target.GetType();

        if (t == typeof(Line))
          target = new LineCurve((Line)target);

        else if (t == typeof(Arc))
          target = new ArcCurve((Arc)target);

        else if (t == typeof(Circle))
          target = new ArcCurve((Circle)target);

        else if (t == typeof(Ellipse))
          target = ((Ellipse)target).ToNurbsCurve();

        else if (t == typeof(Box))
          target = Brep.CreateFromBox((Box)target);

        else if (t == typeof(BoundingBox))
          target = Brep.CreateFromBox((BoundingBox)target);

        else if (t == typeof(Rectangle3d))
          target = ((Rectangle3d)target).ToNurbsCurve();

        else if (target is Polyline)
          target = new PolylineCurve((Polyline)target);
      }

      return toReturn;
    }

    string IGH_TypeHint.TypeName { get { return "ghdoc Object when geometry (rhinoscriptsyntax)"; } }
  }
    */

  [Guid("35915213-5534-4277-81B8-1BDC9E7383D2")]
  public class NoChangeHint : GH_NullHint, IGH_TypeHint
  {
    Guid IGH_TypeHint.HintID { get { return this.GetType().GUID; } }

    string IGH_TypeHint.TypeName { get { return "No Type Hint"; } }
  }




}