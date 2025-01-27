namespace RobotFramework.DotNetLibraryBase.Tests;

public class LibraryInfoTest
{
    readonly LibraryInfo Info = new(typeof(DotNetDemoLibrary.DemoKeywords));

    [Fact]
    public void LibraryConstantsShouldWork()
    {
        Assert.Equal("GLOBAL", Info.Scope);
        Assert.Equal("1.0", Info.Version);
    }

    [Fact]
    public void MethodsShouldFind4Keywords()
    {
        Assert.Equal(5, Info.Keywords.Count);
        Assert.Contains("DoSomething", Info.Keywords.Keys);
        Assert.Contains("DoSomethingWithAnString", Info.Keywords.Keys);
        Assert.Contains("set_AProperty", Info.Keywords.Keys);
        Assert.Contains("get_AProperty", Info.Keywords.Keys);
    }
}
