# pythoneda-shared-pythonlang/shell

shared domain for shell operations

## How to declare it in your flake

python ~/github/pythoneda/pythoneda-tools-artifact/new-domain/pythoneda/tools/artifact/new_domain/application/new_domain_app.py -o pythoneda-shared-python -n shell -t "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" -g "D8DF2D915F27510072DFF42160856541692CA3C3" -p pythoneda.shared.shellox.removeme -d 'shared domain for shell operations'
Check the latest tag of the definition repository: https://github.com/pythoneda-shared-pythonlang-def/shell, and use it instead of the `[version]` placeholder below.

```nix
{
  description = "[..]";
  inputs = rec {
    [..]
    pythoneda-shared-pythonlang-shell = {
      [optional follows]
      url =
        "github:pythoneda-shared-pythonlang-def/shell/[version]";
    };
  };
  outputs = [..]
};
```

Should you use another PythonEDA modules, you might want to pin those also used by this project. The same applies to [https://nixos/nixpkgs](nixpkgs "nixpkgs") and [https://github.com/numtide/flake-utils](flake-utils "flake-utils").

The Nix flake is managed by the [https://github.com/pythoneda-shared-pythonlang-def/shell](shell "shell") definition repository.

Use the specific package depending on your system (one of `flake-utils.lib.defaultSystems`) and Python version:

- `#packages.[system].pythoneda-shared-pythonlang-shell-python38`
- `#packages.[system].pythoneda-shared-pythonlang-shell-python39`
- `#packages.[system].pythoneda-shared-pythonlang-shell-python310`
- `#packages.[system].pythoneda-shared-pythonlang-shell-python311`
