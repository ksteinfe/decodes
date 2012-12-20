using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using Grasshopper.Kernel;
using System.Drawing;
using GhPython.Properties;
using GhPython.Component;

namespace GhPython.Decodes {

    public class Decodes_ColorBakeComponent : SafeComponent {
        public Decodes_ColorBakeComponent()
            //Call the base constructor
            : base("Decodes Properties Bake", "BakeProps", "Bakes geometry with properties parsed from a Decodes _props stream", "Maths", "Script") {
            InitalizePrivateData();
        }

        private List<Rhino.DocObjects.ObjectAttributes> m_att;
        private List<object> m_obj;
        private void InitalizePrivateData() {
            m_att = new List<Rhino.DocObjects.ObjectAttributes>();
            m_obj = new List<object>();
        }

        protected override void RegisterInputParams( GH_Component.GH_InputParamManager pManager ) {
            pManager.Register_GeometryParam("Geometry", "G", "The geometry to bake", GH_ParamAccess.list);
            pManager.Register_StringParam("Properties", "P", "The properties to apply to the geometry when baking.  See the help file for documentation", GH_ParamAccess.list);
        }

        protected override void RegisterOutputParams( GH_Component.GH_OutputParamManager pManager ) {

        }

        protected override void SafeSolveInstance( IGH_DataAccess DA ) {
            List<Grasshopper.Kernel.Types.IGH_GeometricGoo> geom = new List<Grasshopper.Kernel.Types.IGH_GeometricGoo>();
            List<string> propstrings = new List<string>();
            if ((DA.GetDataList(0, geom)) && (DA.GetDataList(1, propstrings)))//if it works...
            {
                if (geom.Count != propstrings.Count) {
                    AddRuntimeMessage(GH_RuntimeMessageLevel.Error, "geometry and property inputs are not lists of the same length.  check your inputs.");
                    return;
                }
                for (int i = 0; i < geom.Count; i++) {
                    Rhino.DocObjects.ObjectAttributes att = PropertyStringToAttributes(propstrings[i]);
                    m_att.Add(att);
                    m_obj.Add(geom[i]);
                }
            }
        }


        private Rhino.DocObjects.ObjectAttributes PropertyStringToAttributes(string propstring) {
            Rhino.DocObjects.ObjectAttributes att = new Rhino.DocObjects.ObjectAttributes();

            att.Name = "Rodrigo";

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


        
        public void Menu_BakeClicked( Object sender, EventArgs e ) {
            Rhino.RhinoDoc rhdoc = Rhino.RhinoDoc.ActiveDoc; //TODO: make sure this is kosher

            for (int n = 0; n < m_obj.Count; n++) {
                object obj = m_obj[n];
                Rhino.DocObjects.ObjectAttributes att = m_att[n];
                if (obj == null) continue;

                Guid id = new Guid();
                
                //Bake to the right type of object
                if (obj is Rhino.Geometry.GeometryBase) {
                    Rhino.Geometry.GeometryBase geomObj = obj as Rhino.Geometry.GeometryBase;

                    switch (geomObj.ObjectType) {
                        case Rhino.DocObjects.ObjectType.Brep:
                            id = rhdoc.Objects.AddBrep(obj as Rhino.Geometry.Brep, att);
                            break;
                        case Rhino.DocObjects.ObjectType.Curve:
                            id = rhdoc.Objects.AddCurve(obj as Rhino.Geometry.Curve, att);
                            break;
                        case Rhino.DocObjects.ObjectType.Point:
                            id = rhdoc.Objects.AddPoint((obj as Rhino.Geometry.Point).Location, att);
                            break;
                        case Rhino.DocObjects.ObjectType.Surface:
                            id = rhdoc.Objects.AddSurface(obj as Rhino.Geometry.Surface, att);
                            break;
                        case Rhino.DocObjects.ObjectType.Mesh:
                            id =  rhdoc.Objects.AddMesh(obj as Rhino.Geometry.Mesh, att);
                            break;
                        //case (Rhino.DocObjects.ObjectType)1073741824://Rhino.DocObjects.ObjectType.Extrusion:
                        //     id = (Guid)typeof(Rhino.DocObjects.Tables.ObjectTable).InvokeMember("AddExtrusion", BindingFlags.Instance | BindingFlags.InvokeMethod, null, doc.Objects, new object[] { obj, att });
                        //    break;
                        case Rhino.DocObjects.ObjectType.PointSet:
                            id = rhdoc.Objects.AddPointCloud(obj as Rhino.Geometry.PointCloud, att); //This is a speculative entry
                            break;
                        default:
                            AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "The component does not know how to handle this type of geometry: " + obj.GetType().FullName);
                            return;
                    }
                } else {
                    
                    Type objectType = obj.GetType();
                    if (obj is Grasshopper.Kernel.IGH_BakeAwareData) {
                        Grasshopper.Kernel.IGH_BakeAwareData bakedata = (Grasshopper.Kernel.IGH_BakeAwareData)obj;
                        bakedata.BakeGeometry(rhdoc, att, out id);
                        return;
                    }
                    /*
                    if (objectType == typeof(Grasshopper.Kernel.Types.GH_Arc)) {
                        id = rhdoc.Objects.AddArc((Rhino.Geometry.Arc)obj, att);
                    } else if (objectType == typeof(Grasshopper.Kernel.Types.GH_Box)) {
                        id = rhdoc.Objects.AddBrep(((Rhino.Geometry.Box)obj).ToBrep(), att);
                    } else if (objectType == typeof(Grasshopper.Kernel.Types.GH_Circle)) {
                        id = rhdoc.Objects.AddCircle((Rhino.Geometry.Circle)obj, att);
                    } else if (objectType == typeof(Grasshopper.Kernel.Types.GH_Curve)) {
                        id = rhdoc.Objects.AddCurve((Rhino.Geometry.Curve)obj, att);
                    } else if (objectType == typeof(Grasshopper.Kernel.Types.GH_Point)) {
                        Grasshopper.Kernel.Types.GH_Point pt = (Grasshopper.Kernel.Types.GH_Point)obj;
                        pt.BakeGeometry(rhdoc, att, ref id);
                    } else if (objectType == typeof(Grasshopper.Kernel.Types.GH_Line)) {
                        id = rhdoc.Objects.AddLine((Rhino.Geometry.Line)obj, att);
                    } else if (objectType == typeof(Grasshopper.Kernel.Types.GH_Vector)) {
                        AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "I'm not sure how you'd like me to bake a vector");
                        return;
                    } else {
                        AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "The component does not know how to handle this type of gh_geometry: " + objectType.FullName);
                        return;
                    }
                     */
                }

                //if (groupIndex != -1)  doc.Groups.AddToGroup(groupIndex, id);

            }
        }
        

        public override bool AppendMenuItems( ToolStripDropDown menu ) {
            Menu_AppendObjectName(menu);
            Menu_AppendPreviewItem(menu);
            Menu_AppendEnableItem(menu);

            Menu_AppendSeparator(menu);

            //Menu_AppendBakeItem(menu);
            Menu_AppendItem(menu, "Bake with Properties", Menu_BakeClicked, true);

            Menu_AppendSeparator(menu);

            Menu_AppendWarningsAndErrors(menu);
            Menu_AppendObjectHelp(menu);
            return true;
        }

        public override Guid ComponentGuid { get { return new Guid("{D07CA105-E537-494F-BEA7-E08DDDFC0AB2}"); } }
        protected override Bitmap Icon { get { return Resources.python; } }

    }

}
