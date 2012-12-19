using System.Drawing;
using System.Reflection;
using GhPython.Properties;
using Grasshopper.Kernel;

namespace GhPython
{
  // Supposedly used to show extra information in Grasshopper about
  // this component, but I can't find where this data shows up.
  public class PythonPluginInfo : GH_AssemblyInfo
  {
    public override string Description
    {
      get { return "Decodes Python interpreter component for grasshopper"; }
    }

    public override Bitmap Icon
    {
      get { return Resources.python; }
    }

    public override string Name
    {
      get { return "Decodes Python Interpreter"; }
    }

    public override string Version
    {
      get { return Assembly.GetExecutingAssembly().GetName().Version.ToString(); }
    }

    public override string AuthorName
    {
      get { return "Kyle Steinfeld (stolen from Robert McNeel and Associates)"; }
    }

    public override string AuthorContact
    {
      get { return "ksteinfe@berkeley.edu"; }
    }

    public override GH_LibraryLicense License
    {
      get { return GH_LibraryLicense.opensource; }
    }
  }
}