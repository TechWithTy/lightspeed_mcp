"""
A comprehensive MCP tool demonstrating all Context features:
- Logging (debug, info, warning, error)
- Progress reporting at multiple stages
- Resource access
- All available context attributes
- LLM sampling
- Returns a summary of all context features/values
"""
from fastmcp import mcp, Context

@mcp.tool()
async def context_kitchen_sink_demo(uri: str, ctx: Context) -> dict:
    results = {}
    await ctx.debug("Debug log: starting kitchen sink demo.")
    await ctx.info("Info log: kitchen sink demo running.")
    await ctx.warning("Warning log: this is a warning.")
    await ctx.error("Error log: this is a simulated error.")

    await ctx.report_progress(1, 5)
    resource = await ctx.read_resource(uri)
    results['resource_content'] = resource[0].content if resource else None
    await ctx.report_progress(2, 5)

    results['request_id'] = getattr(ctx, 'request_id', None)
    results['client_id'] = getattr(ctx, 'client_id', None)
    results['user'] = getattr(ctx, 'user', None)
    results['session'] = getattr(ctx, 'session', None)
    results['agent'] = getattr(ctx, 'agent', None)
    results['roots'] = getattr(ctx, 'roots', None)
    results['metadata'] = getattr(ctx, 'metadata', None)
    await ctx.report_progress(3, 5)

    sample_result = await ctx.sample("Say hello to the world.")
    results['llm_sample'] = sample_result.text if hasattr(sample_result, 'text') else str(sample_result)
    await ctx.report_progress(4, 5)

    results['all_ctx_attributes'] = {k: getattr(ctx, k, None) for k in dir(ctx) if not k.startswith('_') and not callable(getattr(ctx, k, None))}
    await ctx.report_progress(5, 5)

    return results
