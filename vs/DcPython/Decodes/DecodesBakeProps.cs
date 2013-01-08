using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Data;
using System.Drawing;
using DcPython.Properties;
using GhPython.Component;

namespace DcPython.Decodes
{

    public class Decodes_ColorBakeComponent : SafeComponent
    {
        //TODO: bake with materials, handle layers, if only get one object do not group

        public Decodes_ColorBakeComponent()
            //Call the base constructor
            : base("Decodes Hard Boil", "HardBoil", "Boils geometry with properties parsed from a Decodes _props stream", "Maths", "Decodes")
        {
            InitalizePrivateData();
            Params.ParameterChanged += ParameterChanged;

            this.IconDisplayMode = GH_IconDisplayMode.icon;
        }
        //Rhino.DocObjects.ObjectAttributes
        private List<Decodes_Attributes> m_att;
        private List<Grasshopper.Kernel.Types.IGH_GeometricGoo> m_obj;
        private List<string> required_layers;
        private List<int> m_branch_index;
        public string parent_layer_name = "decodes";

        private void InitalizePrivateData()
        {
            m_att = new List<Decodes_Attributes>();
            m_obj = new List<Grasshopper.Kernel.Types.IGH_GeometricGoo>();
            m_branch_index = new List<int>();
            required_layers = new List<string>();
        }
        private void ParameterChanged(object sender, GH_ParamServerEventArgs e) { InitalizePrivateData(); ClearData(); }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.Register_GenericParam("Geometry", "geom", "The geometry to bake", GH_ParamAccess.tree);
            pManager.RegisterParam(new GHParam_Decodes_Attributes(), "Properties", "props", "The properties to apply to the geometry when baking.  See the help file for documentation", GH_ParamAccess.tree);
        }

        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {

        }

        protected override void SafeSolveInstance(IGH_DataAccess DA)
        {
            this.InitalizePrivateData();
            GH_Structure<Grasshopper.Kernel.Types.IGH_Goo> geom_tree = new GH_Structure<Grasshopper.Kernel.Types.IGH_Goo>();
            GH_Structure<Decodes_Attributes> attr_tree = new GH_Structure<Decodes_Attributes>();
            if ((DA.GetDataTree<Grasshopper.Kernel.Types.IGH_Goo>(0, out geom_tree)) && (DA.GetDataTree<Decodes_Attributes>(1, out attr_tree)))
            {
                if (geom_tree.PathCount != attr_tree.Branches.Count) { AddRuntimeMessage(GH_RuntimeMessageLevel.Error, "geometry and property inputs do not have the same number of branches.  check your inputs."); return; }

                for (int b = 0; b < geom_tree.Branches.Count; b++)
                {
                    List<Grasshopper.Kernel.Types.IGH_Goo> geom_given = geom_tree.Branches[b];
                    List<Decodes_Attributes> attr_given = attr_tree.Branches[b];

                    if (geom_given.Count != attr_given.Count) { AddRuntimeMessage(GH_RuntimeMessageLevel.Error, "geometry and property inputs are not lists of the same length.  check your inputs."); return; }

                    for (int i = 0; i < geom_given.Count; i++)
                    {
                        if (!(geom_given[i] is Grasshopper.Kernel.Types.IGH_GeometricGoo)) { AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "Did you give me something that isn't geometry?"); continue; }
                        try
                        {
                            m_obj.Add((Grasshopper.Kernel.Types.IGH_GeometricGoo)geom_given[i]);
                            if (!(attr_given[i] is Decodes_Attributes)) m_att.Add(new Decodes_Attributes());
                            else
                            {
                                m_att.Add(attr_given[i]);
                                if (!required_layers.Contains(attr_given[i].layer)) required_layers.Add(attr_given[i].layer);
                            }
                            m_branch_index.Add(b);
                        }
                        catch (Exception e)
                        {
                            AddRuntimeMessage(GH_RuntimeMessageLevel.Error, "Did you give me something that looks like geometry, but isn't?\n" + e.Message);
                        }

                    }
                }
            }
        }

        public override void DrawViewportWires(IGH_PreviewArgs args)
        {
            //base.DrawViewportWires(args);
            int defaultPointRadius = 2;

            for (int n = 0; n < m_obj.Count; n++)
            {
                object obj = m_obj[n];
                Rhino.DocObjects.ObjectAttributes att = m_att[n].Value;
                if (obj == null) continue;
                Type objectType = obj.GetType();
                if (objectType == typeof(Grasshopper.Kernel.Types.GH_Vector))
                {
                    Rhino.Geometry.Vector3d rh_vec = ((Grasshopper.Kernel.Types.GH_Vector)obj).Value;
                    args.Display.DrawArrow(new Rhino.Geometry.Line(new Rhino.Geometry.Point3d(0, 0, 0), new Rhino.Geometry.Point3d(rh_vec)), att.ObjectColor);
                    continue;
                }
                if (objectType == typeof(Grasshopper.Kernel.Types.GH_Point))
                {
                    Rhino.Geometry.Point3d rh_point = ((Grasshopper.Kernel.Types.GH_Point)obj).Value;
                    if (att.PlotWeight == 0) args.Display.DrawPoint(rh_point, Rhino.Display.PointStyle.Simple, defaultPointRadius, att.ObjectColor);
                    else args.Display.DrawPoint(rh_point, Rhino.Display.PointStyle.Simple, (int)att.PlotWeight, att.ObjectColor);
                    continue;
                }
                if (objectType == typeof(Grasshopper.Kernel.Types.GH_Line))
                {
                    Rhino.Geometry.Line rh_line = ((Grasshopper.Kernel.Types.GH_Line)obj).Value;
                    if (att.PlotWeight == 0) args.Display.DrawLine(rh_line, att.ObjectColor);
                    else args.Display.DrawLine(rh_line, att.ObjectColor, (int)att.PlotWeight);
                    continue;
                }
                if (objectType == typeof(Grasshopper.Kernel.Types.GH_Mesh))
                {
                    Rhino.Geometry.Mesh rh_mesh = ((Grasshopper.Kernel.Types.GH_Mesh)obj).Value;
                    Rhino.Display.DisplayMaterial mat = new Rhino.Display.DisplayMaterial(att.ObjectColor, 0.5);
                    args.Display.DrawMeshShaded(rh_mesh, mat);
                    continue;
                }
                if (objectType == typeof(Grasshopper.Kernel.Types.GH_Curve))
                {
                    //TODO: deal with open polylines, curves, non-planar polycurves, etc
                    Rhino.Geometry.Curve rh_curve = ((Grasshopper.Kernel.Types.GH_Curve)obj).Value;

                    Rhino.Geometry.Polyline rh_pline = new Rhino.Geometry.Polyline();
                    if ((rh_curve.IsClosed) && (rh_curve.IsPlanar()) && (rh_curve.TryGetPolyline(out rh_pline)))
                    {
                        bool fill = true;
                        Rhino.Geometry.Intersect.CurveIntersections iev = Rhino.Geometry.Intersect.Intersection.CurveSelf(rh_curve, Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance);
                        if (iev.Count > 0)
                        {
                            AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "Found a self-intersecting polygon.  Fills will not be applied.");
                            fill = false;
                        }
                        args.Display.DrawPolygon(rh_pline, att.ObjectColor, false);

                        if (fill)
                        {
                            Rhino.Geometry.Mesh m = Rhino.Geometry.Mesh.CreateFromPlanarBoundary(rh_curve, Rhino.Geometry.MeshingParameters.Smooth);
                            args.Display.DrawMeshShaded(m, new Rhino.Display.DisplayMaterial(att.ObjectColor, 0.5));
                        }
                        continue;
                    }
                }

                AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "The component does not know how to handle this type of gh_geometry: " + objectType.FullName);
            }

        }


        private void BakeStoredObjects(Rhino.RhinoDoc rhdoc)
        {
            // do we need to add layers?
            int parent_index = rhdoc.Layers.Find(parent_layer_name, true);
            if (parent_index < 0) parent_index = rhdoc.Layers.Add(parent_layer_name, Color.White);

            Dictionary<string, int> layer_dict = new Dictionary<string, int>();
            if (rhdoc.Layers[parent_index].GetChildren() != null) foreach (Rhino.DocObjects.Layer l in rhdoc.Layers[parent_index].GetChildren()) layer_dict.Add(l.Name, l.LayerIndex);

            foreach (string layername in required_layers)
                if (!layer_dict.ContainsKey(layername))
                {
                    Rhino.DocObjects.Layer childlayer = new Rhino.DocObjects.Layer();
                    childlayer.ParentLayerId = rhdoc.Layers[parent_index].Id;
                    childlayer.Name = layername;
                    int index = rhdoc.Layers.Add(childlayer);
                    if (index < 0) AddRuntimeMessage(GH_RuntimeMessageLevel.Error, "Layer creation gone bad!");
                    layer_dict.Add(layername, index);
                }

            int group_index = -1;
            List<Guid> guids = new List<Guid>();
            int current_branch_index = -1;
            for (int n = 0; n < m_obj.Count; n++)
            {
                if (m_branch_index[n] != current_branch_index)
                {
                    group_index = rhdoc.Groups.Add();
                    current_branch_index = m_branch_index[n];
                }
                object obj = m_obj[n];
                Rhino.DocObjects.ObjectAttributes att = m_att[n].Value;
                att.LayerIndex = layer_dict[m_att[n].layer];
                if (obj == null) continue;

                Guid id = new Guid();

                Type objectType = obj.GetType();
                if (objectType == typeof(Grasshopper.Kernel.Types.GH_Vector)) { AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "Vectors are confusing things to bake - I'll just make a point at the vector position.  If you want to visualize a 'positioned' vector, try giving me a Ray instead."); }
                if (obj is Grasshopper.Kernel.IGH_BakeAwareData)
                {
                    Grasshopper.Kernel.IGH_BakeAwareData bakedata = (Grasshopper.Kernel.IGH_BakeAwareData)obj;
                    bakedata.BakeGeometry(rhdoc, att, out id);
                    rhdoc.Groups.AddToGroup(group_index, id);
                    if (guids != null) guids.Add(id);


                    // draw fill meshes for closed planar curves
                    if (objectType == typeof(Grasshopper.Kernel.Types.GH_Curve))
                    {
                        Rhino.Geometry.Curve rh_curve = ((Grasshopper.Kernel.Types.GH_Curve)obj).Value;
                        if ((rh_curve.IsClosed) && (rh_curve.IsPlanar()))
                        {
                            Rhino.Geometry.Intersect.CurveIntersections iev = Rhino.Geometry.Intersect.Intersection.CurveSelf(rh_curve, Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance);
                            if (iev.Count == 0){
                                Rhino.Geometry.Mesh mesh = Rhino.Geometry.Mesh.CreateFromPlanarBoundary(rh_curve, Rhino.Geometry.MeshingParameters.Smooth);
                                Grasshopper.Kernel.IGH_BakeAwareData meshbakedata = (Grasshopper.Kernel.IGH_BakeAwareData) new Grasshopper.Kernel.Types.GH_Mesh(mesh);
                                att.PlotWeight = 0.0;
                                meshbakedata.BakeGeometry(rhdoc, att, out id);
                                rhdoc.Groups.AddToGroup(group_index, id);
                                if (guids != null) guids.Add(id);
                            }
                        }
                    }

                    continue;
                }
                else
                {
                    AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "The component does not know how to handle this type of gh_geometry: " + objectType.FullName);
                    continue;
                }
                //if (groupIndex != -1)  doc.Groups.AddToGroup(groupIndex, id);
            }

            rhdoc.Views.Redraw();
        }


        public override bool AppendMenuItems(ToolStripDropDown menu)
        {
            Menu_AppendObjectNameEx(menu);
            Menu_AppendPreviewItem(menu);
            Menu_AppendEnableItem(menu);

            Menu_AppendSeparator(menu);

            Menu_AppendItem(menu, "Hard Boil", Menu_BakeClicked, Resources.Icons_Component_Preview, true, false);
            Menu_AppendSeparator(menu);

            Menu_AppendItem(menu, "Boil to Layer:");
            Menu_AppendTextItem(menu, parent_layer_name, Menu_ParentLayerNameKeyDown, Menu_ParentLayerNameChanged, true);

            Menu_AppendSeparator(menu);

            Menu_AppendWarningsAndErrors(menu);
            Menu_AppendObjectHelp(menu);
            return true;
        }

        public void Menu_BakeClicked(Object sender, EventArgs e)
        {
            Rhino.RhinoDoc rhdoc = Rhino.RhinoDoc.ActiveDoc;
            BakeStoredObjects(rhdoc);
        }

        private void Menu_ParentLayerNameKeyDown(Object sender, EventArgs e) { Menu_ParentLayerNameChanged(sender, ((Grasshopper.GUI.GH_MenuTextBox)sender).Text); }
        public void Menu_ParentLayerNameChanged(Object sender, string text) { this.parent_layer_name = text; }

        public override Guid ComponentGuid { get { return new Guid("{D07CA105-E537-494F-BEA7-E08DDDFC0AB2}"); } }
        protected override Bitmap Icon { get { return Resources.Icons_Component_Preview; } }

    }

}
