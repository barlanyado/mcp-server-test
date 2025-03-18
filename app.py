# markdown_server.py
import argparse
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("MarkdownFormatter")

@mcp.tool()
def format_markdown(text: str, headings: bool = True, bold: bool = True, 
                   italics: bool = True, code_blocks: bool = True) -> str:
    """
    Format plain text into markdown by adding common markdown syntax.
    
    Args:
        text: The plain text to format
        headings: Whether to convert lines that look like headings (default: True)
        bold: Whether to emphasize certain phrases with bold formatting (default: True)
        italics: Whether to convert phrases in quotes to italics (default: True)
        code_blocks: Whether to format indented text as code blocks (default: True)
    
    Returns:
        The formatted markdown text
    """
    lines = text.split('\n')
    result = []
    
    in_code_block = False
    
    for line in lines:
        # Check for headings (lines ending with : or starting with "Section", "Chapter", etc.)
        if headings and (line.endswith(':') or 
                         any(line.startswith(prefix) for prefix in ["Section", "Chapter", "Part"])):
            # Make it a heading level 2
            line = f"## {line}"
        
        # Check for code blocks (4 spaces or tab indentation)
        if code_blocks and (line.startswith('    ') or line.startswith('\t')):
            if not in_code_block:
                result.append('```')
                in_code_block = True
            # Remove the indentation
            line = line.removeprefix('    ').removeprefix('\t')
        elif in_code_block:
            result.append('```')
            in_code_block = False
        
        # Process bold formatting (words in ALL CAPS)
        if bold:
            words = line.split()
            for i, word in enumerate(words):
                if word.isupper() and len(word) > 1:
                    words[i] = f"**{word}**"
            line = ' '.join(words)
        
        # Process italics (text in quotes)
        if italics:
            import re
            line = re.sub(r'"([^"]+)"', r'*\1*', line)
        
        result.append(line)
    
    # Close any open code block
    if in_code_block:
        result.append('```')
    
    return '\n'.join(result)

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Markdown Formatter MCP Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=3000, help="Port to bind the server to")
    parser.add_argument("--transport", default="stdio", choices=["stdio", "sse"], 
                        help="Transport type (stdio or sse)")
    
    args = parser.parse_args()
    
    # Run the server with the specified options
    if args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")
