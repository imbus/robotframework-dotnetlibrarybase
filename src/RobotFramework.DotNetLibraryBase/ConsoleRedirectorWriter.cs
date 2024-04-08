using System.Text;

namespace RobotFramework.DotNetLibraryBase;

public class ConsoleRedirectorWriter : TextWriter
{
    public ConsoleRedirectorWriter(string? encoding)
    {
        if (encoding != null)
            Encoding = Encoding.GetEncoding(encoding);
        else
            Encoding = Encoding.Default;
    }
    public override Encoding Encoding { get; }

    public override void Write(char value)
    {
        WriteChar(value);
    }

    protected virtual void WriteChar(char value)
    {

    }
}
