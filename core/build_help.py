# Library Imports


# Local Imports
from core.command import Command


def build_help(command: Command) -> str:
    """Builds a help menu for a Command.

    Assumptions:
      - command.args is a dict[str, Arg] keyed by arg.name
      - command.kwargs is a dict[str, Kwarg] keyed by kwarg.name
      - Arg/Kwarg may be class-based specs (name/description set on class), so we use getattr safely
    """
    name = getattr(command, "name", "<unnamed>")
    desc = getattr(command, "description", "") or ""
    extra_help = getattr(command, "help", "") or ""

    args = getattr(command, "args", None) or {}
    kwargs = getattr(command, "kwargs", None) or {}
    required_context = getattr(command, "required_context", None) or set()

    def _fmt_aliases(aliases) -> str:
        aliases = [a for a in (aliases or []) if a]
        return f" (aliases: {', '.join(aliases)})" if aliases else ""

    def _arg_meta(obj):
        # supports either instances or class-specs
        return (
            getattr(obj, "name", None),
            getattr(obj, "description", "") or "",
            getattr(obj, "aliases", []) or [],
        )

    def _wrap(text: str, width: int = 84, indent: str = "  ") -> str:
        if not text:
            return ""
        words = text.split()
        lines, line = [], ""
        for w in words:
            if len(line) + len(w) + (1 if line else 0) > width:
                lines.append(line)
                line = w
            else:
                line = f"{line} {w}".strip()
        if line:
            lines.append(line)
        return "\n".join(indent + ln for ln in lines)

    # Usage line
    usage_parts = [name]
    if args:
        # show positional args in order (sorted by key for stability)
        for arg_key in sorted(args.keys()):
            usage_parts.append(f"<{arg_key}>")
    if kwargs:
        usage_parts.append("[options]")
    usage = " ".join(usage_parts)

    # Build sections
    lines: list[str] = []
    lines.append("COMMAND")
    lines.append(f"  {name}")
    lines.append("")
    lines.append("USAGE")
    lines.append(f"  {usage}")
    lines.append("")
    lines.append("DESCRIPTION")
    lines.append(_wrap(desc) or "  (no description)")
    lines.append("")


    if args:
        lines.append("POSITIONAL ARGUMENTS")
        # stable order; if you later add an explicit order field, change here
        for key in sorted(args.keys()):
            obj = args[key]
            a_name, a_desc, a_aliases = _arg_meta(obj)
            display = a_name or key
            lines.append(f"  {display}{_fmt_aliases(a_aliases)}")
            if a_desc:
                lines.append(_wrap(a_desc, indent="    "))
            else:
                lines.append("    (no description)")
    lines.append("")


    if kwargs:
        lines.append("OPTIONS")
        # sort by option name
        for key in sorted(kwargs.keys()):
            obj = kwargs[key]
            k_name, k_desc, k_aliases = _arg_meta(obj)
            opt = k_name or key

            # show common CLI style: --long, -short (from aliases)
            # If aliases are stored without dashes (e.g. "ah"), we add "-" for 1-char and "--" for >1?
            # Your examples look like {"ah"}; we’ll render as "-ah" by default.
            pretty_aliases = []
            for a in (k_aliases or []):
                if a.startswith("-"):
                    pretty_aliases.append(a)
                else:
                    pretty_aliases.append(f"-{a}")
            alias_str = f" (aliases: {', '.join(pretty_aliases)})" if pretty_aliases else ""

            # render main option as --name
            main_flag = opt if opt.startswith("-") else f"--{opt}"
            lines.append(f"  {main_flag}{alias_str}")
            if k_desc:
                lines.append(_wrap(k_desc, indent="    "))
            else:
                lines.append("    (no description)")
    lines.append("")

    if required_context:
        # render set contents nicely
        lines.append("REQUIRED CONTEXT")
        ctx_items = sorted(str(x) for x in required_context)
        for item in ctx_items:
            lines.append(f"  - {item}")
    lines.append("")

    # Extra developer-provided help text
    if extra_help.strip():
        lines.append("NOTES")
        lines.append(_wrap(extra_help.strip()) or "")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"