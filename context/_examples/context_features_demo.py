"""
Demonstrates all major features of the FastMCP Context object:
- Logging (debug/info/warning/error)
- Progress reporting
- Resource access
- Request/client info
- LLM sampling
"""
from fastmcp import Context, mcp


@mcp.tool()
async def context_feature_demo(uri: str, ctx: Context) -> dict:
    """Showcase all Context features in a single tool."""
    results = {}
    await ctx.debug("Debug log: starting context demo.")
    await ctx.info("Info log: context demo running.")
    await ctx.warning("Warning log: this is a warning.")
    await ctx.error("Error log: this is a simulated error.")

    # Progress reporting
    await ctx.report_progress(1, 5)
    # Resource access (simulate text resource)
    resource = await ctx.read_resource(uri)
    results['resource_content'] = resource[0].content if resource else None
    await ctx.report_progress(2, 5)

    # Request info: all available attributes
    results['request_id'] = getattr(ctx, 'request_id', None)
    results['client_id'] = getattr(ctx, 'client_id', None)
    results['user'] = getattr(ctx, 'user', None)
    results['session'] = getattr(ctx, 'session', None)
    results['agent'] = getattr(ctx, 'agent', None)
    results['roots'] = getattr(ctx, 'roots', None)
    results['metadata'] = getattr(ctx, 'metadata', None)
    await ctx.report_progress(3, 5)

    # LLM sampling (simulate prompt)
    sample_result = await ctx.sample("Say hello to the world.")
    results['llm_sample'] = sample_result.text if hasattr(sample_result, 'text') else str(sample_result)
    await ctx.report_progress(4, 5)

    # Show all context object attributes (for demo)
    results['all_ctx_attributes'] = {k: getattr(ctx, k, None) for k in dir(ctx) if not k.startswith('_') and not callable(getattr(ctx, k, None))}
    await ctx.report_progress(5, 5)

    return results
