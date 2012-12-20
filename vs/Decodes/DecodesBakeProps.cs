using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using Grasshopper.Kernel;
using System.Drawing;
using DcPython.Properties;
using GhPython.Component;

namespace DcPython.Decodes
{

    public class Decodes_ColorBakeComponent : SafeComponent
    {
        public Decodes_ColorBakeComponent()
            //Call the base constructor
            : base("Decodes Properties Bake", "BakeProps", "Bakes geometry with properties parsed from a Decodes _props stream", "Maths", "Script")
        {
            InitalizePrivateData();
        }

        private List<Rhino.DocObjects.ObjectAttributes> m_att;
        private List<object> m_obj;
        private void InitalizePrivateData()
        {
            m_att = new List<Rhino.DocObjects.ObjectAttributes>();
            m_obj = new List<object>();
        }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.Register_GeometryParam("Geometry", "G", "The geometry to bake", GH_ParamAccess.list);
            pManager.Register_StringParam("Properties", "P", "The properties to apply to the geometry when baking.  See the help file for documentation", GH_ParamAccess.list);
        }

        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {

        }

        protected override void SafeSolveInstance(IGH_DataAccess DA)
        {
            this.InitalizePrivateData();
            List<Grasshopper.Kernel.Types.IGH_GeometricGoo> geom = new List<Grasshopper.Kernel.Types.IGH_GeometricGoo>();
            List<string> propstrings = new List<string>();
            if ((DA.GetDataList(0, geom)) && (DA.GetDataList(1, propstrings)))//if it works...
            {
                if (geom.Count != propstrings.Count)
                {
                    AddRuntimeMessage(GH_RuntimeMessageLevel.Error, "geometry and property inputs are not lists of the same length.  check your inputs.");
                    return;
                }
                for (int i = 0; i < geom.Count; i++)
                {
                    Rhino.DocObjects.ObjectAttributes att = PropertyStringToAttributes(propstrings[i]);
                    m_att.Add(att);
                    m_obj.Add(geom[i]);
                }
            }
        }

        System.Drawing.Color defaultColor = Color.Black;
        int defaultPointRadius = 2;

        private Rhino.DocObjects.ObjectAttributes PropertyStringToAttributes(string propstring)
        {
            Rhino.DocObjects.ObjectAttributes att = new Rhino.DocObjects.ObjectAttributes();

            Dictionary<string, string> propdict = new Dictionary<string, string>();
            foreach (string pair in propstring.Split(new string[] { "::" }, StringSplitOptions.RemoveEmptyEntries))
            {
                string[] keyval = pair.Split(new char[] { '=' });
                propdict.Add(keyval[0], keyval[1]);
            }
            if (propdict.ContainsKey("name")) att.Name = propdict["name"];

            att.PlotWeight = 0.0; // 0 tells rhino to use the default plot width
            att.PlotWeightSource = Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromObject;
            if (propdict.ContainsKey("weight"))
            {
                try  {att.PlotWeight = float.Parse(propdict["weight"]); } 
                catch  {AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "Trouble parsing a weight string" + propdict["weight"]); }
            }

            att.ObjectColor = defaultColor;
            att.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject;
            att.PlotColorSource = Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromDisplay;
            if (propdict.ContainsKey("color"))
            {
                try
                {
                    string[] rgb = propdict["color"].Substring(6).TrimEnd(new char[] { ']' }).Split(new char[] { ',' });
                    System.Drawing.Color c = Color.FromArgb((int)(float.Parse(rgb[0]) * 255), (int)(float.Parse(rgb[1]) * 255), (int)(float.Parse(rgb[2]) * 255));
                    att.ObjectColor = c;
                }
                catch
                {
                    AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "Trouble parsing a color string" + propdict["color"]);
                }
            }
            return att;
        }

        /*
        private void Bake() {

            //int groupIndex = -1;
            //if (groupListTgthr)
            //    groupIndex = doc.Groups.Add();

            for (int i = 0; i < objs.Count; i++) {
                object obj = objs[i];
                if (obj == null) { return; }

                //Make new attribute to set name
                Rhino.DocObjects.ObjectAttributes att = new Rhino.DocObjects.ObjectAttributes();

                string name = names.Count > 0 ? names[i % names.Count] : null;
                //Set object name
                if (!string.IsNullOrEmpty(name)) {
                    att.Name = name;
                }

                Color color = colors.Count > 0 ? colors[i % colors.Count] : new Color();
                //Set color
                if (!color.IsEmpty) {
                    att.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject; //Make the color type "by object"
                    att.ObjectColor = color;

                    att.PlotColorSource = Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromObject; //Make the plot color type "by object"
                    att.PlotColor = color;
                }

                string layer = layers.Count > 0 ? layers[i % layers.Count] : null;
                //Set layer
                if (!string.IsNullOrEmpty(layer) && Rhino.DocObjects.Layer.IsValidName(layer)) {
                    //Get the current layer index
                    Rhino.DocObjects.Tables.LayerTable layerTable = doc.Layers;
                    int layerIndex = layerTable.Find(layer, true);

                    if (layerIndex < 0) //This layer does not exist, we add it
                        {
                        Rhino.DocObjects.Layer onlayer = new Rhino.DocObjects.Layer(); //Make a new layer
                        onlayer.Name = layer;

                        layerIndex = layerTable.Add(onlayer); //Add the layer to the layer table
                        if (layerIndex > -1) //We manged to add layer!
                        {
                            att.LayerIndex = layerIndex;
                            Print("Added new layer to the document at position " + layerIndex + " named " + layer + ". ");
                        } else
                            Print("Layer did not add. Try cleaning up your layers."); //This never happened to me.
                    } else
                        att.LayerIndex = layerIndex; //We simply add to the existing layer
                }


                double pWidth = pWidths.Count > 0 ? pWidths[i % pWidths.Count] : 0;
                //Set plotweight
                if (pWidth > 0) {
                    att.PlotWeightSource = Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromObject;
                    att.PlotWeight = pWidth;
                }


                object material = materials.Count > 0 ? materials[i % materials.Count] : null;
                //Set material
                bool materialByName = !string.IsNullOrEmpty(material as string);
                Rhino.Display.DisplayMaterial inMaterial = material as Rhino.Display.DisplayMaterial;
                if (material is Color) {
                    inMaterial = new Rhino.Display.DisplayMaterial((Color)material);
                }
                if (material != null && inMaterial == null && !materialByName) {
                    if (!(material is string)) {
                        try //We also resort to try with IConvertible
                        {
                            inMaterial = (Rhino.Display.DisplayMaterial)Convert.ChangeType(material, typeof(Rhino.Display.DisplayMaterial));
                        } catch (InvalidCastException) {
                        }
                    }
                }
                if (inMaterial != null || materialByName) {
                    string matName;

                    if (!materialByName) {
                        matName = string.Format("A:{0}-D:{1}-E:{2}-S:{3},{4}-T:{5}",
                          Format(inMaterial.Ambient),
                          Format(inMaterial.Diffuse),
                          Format(inMaterial.Emission),
                          Format(inMaterial.Specular),
                          inMaterial.Shine.ToString(),
                          inMaterial.Transparency.ToString()
                          );
                    } else {
                        matName = (string)material;
                    }

                    int materialIndex = doc.Materials.Find(matName, true);
                    if (materialIndex < 0 && !materialByName) //Material does not exist and we have its specs
          {
                        materialIndex = doc.Materials.Add(); //Let's add it
                        if (materialIndex > -1) {
                            Print("Added new material at position " + materialIndex + " named \"" + matName + "\". ");
                            Rhino.DocObjects.Material m = doc.Materials[materialIndex];
                            m.Name = matName;
                            m.AmbientColor = inMaterial.Ambient;
                            m.DiffuseColor = inMaterial.Diffuse;
                            m.EmissionColor = inMaterial.Emission;
                            //m.ReflectionColor = no equivalent
                            m.SpecularColor = inMaterial.Specular;
                            m.Shine = inMaterial.Shine;
                            m.Transparency = inMaterial.Transparency;
                            //m.TransparentColor = no equivalent
                            m.CommitChanges();

                            att.MaterialSource = Rhino.DocObjects.ObjectMaterialSource.MaterialFromObject;
                            att.MaterialIndex = materialIndex;
                        } else
                            Print("Material did not add. Try cleaning up your materials."); //This never happened to me.
                    } else if (materialIndex < 0 && materialByName) //Material does not exist and we do not have its specs. We do nothing
          {
                        Print("Warning: material name not found. I cannot set the source to this material name. Add a material with name: " + matName);
                    } else {
                        //If this material exists, we do not replace it!
                        att.MaterialSource = Rhino.DocObjects.ObjectMaterialSource.MaterialFromObject;
                        att.MaterialIndex = materialIndex;
                    }
                }


                int wires = wiresEach.Count > 0 ? wiresEach[i % wiresEach.Count] : 0;
                //Set wire density
                if (wires == -1 || wires > 0) {
                    att.WireDensity = wires;
                }

                Bake(obj, att, groupIndex);
            }


        }
         * */


        public override void DrawViewportWires(IGH_PreviewArgs args)
        {
            //base.DrawViewportWires(args);
            for (int n = 0; n < m_obj.Count; n++)
            {
                object obj = m_obj[n];
                Rhino.DocObjects.ObjectAttributes att = m_att[n];
                if (obj == null) continue;
                Type objectType = obj.GetType();
                if (objectType == typeof(Grasshopper.Kernel.Types.GH_Vector))
                {
                    Rhino.Geometry.Vector3d rh_vec = ((Grasshopper.Kernel.Types.GH_Vector) obj).Value;
                    args.Display.DrawArrow(new Rhino.Geometry.Line(new Rhino.Geometry.Point3d(0,0,0),new Rhino.Geometry.Point3d(rh_vec)),att.ObjectColor);
                    continue;
                }
                if (objectType == typeof(Grasshopper.Kernel.Types.GH_Point))
                {
                    Rhino.Geometry.Point3d rh_point = ((Grasshopper.Kernel.Types.GH_Point)obj).Value;
                    if (att.PlotWeight == 0) args.Display.DrawPoint(rh_point, Rhino.Display.PointStyle.Simple, defaultPointRadius, att.ObjectColor);
                    else args.Display.DrawPoint(rh_point, Rhino.Display.PointStyle.Simple, (int) att.PlotWeight, att.ObjectColor);
                    continue;
                }
                if (objectType == typeof(Grasshopper.Kernel.Types.GH_Line))
                {
                    Rhino.Geometry.Line rh_line = ((Grasshopper.Kernel.Types.GH_Line)obj).Value;
                    if (att.PlotWeight == 0) args.Display.DrawLine(rh_line, att.ObjectColor);
                    else args.Display.DrawLine(rh_line, att.ObjectColor, (int)att.PlotWeight);
                    continue;
                }

                AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "The component does not know how to handle this type of gh_geometry: " + objectType.FullName);
            }
        }

        public void Menu_BakeClicked(Object sender, EventArgs e)
        {
            Rhino.RhinoDoc rhdoc = Rhino.RhinoDoc.ActiveDoc;
            BakeStoredObjects(rhdoc);
        }

        private void BakeStoredObjects(Rhino.RhinoDoc rhdoc)
        {
            List<Guid> guids = new List<Guid>();
            for (int n = 0; n < m_obj.Count; n++)
            {
                object obj = m_obj[n];
                Rhino.DocObjects.ObjectAttributes att = m_att[n];
                if (obj == null) continue;

                Guid id = new Guid();

                Type objectType = obj.GetType();
                if (objectType == typeof(Grasshopper.Kernel.Types.GH_Vector)) { AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "Vectors are confusing things to bake - I'll just make a point at the vector position.  If you want to visualize a 'positioned' vector, try giving me a Ray instead."); }
                if (obj is Grasshopper.Kernel.IGH_BakeAwareData)
                {
                    Grasshopper.Kernel.IGH_BakeAwareData bakedata = (Grasshopper.Kernel.IGH_BakeAwareData)obj;
                    bakedata.BakeGeometry(rhdoc, att, out id);
                    if (guids != null) guids.Add(id);
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
            Menu_AppendObjectName(menu);
            Menu_AppendPreviewItem(menu);
            Menu_AppendEnableItem(menu);

            Menu_AppendSeparator(menu);

            //Menu_AppendBakeItem(menu);
            Menu_AppendItem(menu, "Bake", Menu_BakeClicked, true);

            Menu_AppendSeparator(menu);

            Menu_AppendWarningsAndErrors(menu);
            Menu_AppendObjectHelp(menu);
            return true;
        }

        public override Guid ComponentGuid { get { return new Guid("{D07CA105-E537-494F-BEA7-E08DDDFC0AB2}"); } }
        protected override Bitmap Icon { get { return Resources.python; } }

    }

}
