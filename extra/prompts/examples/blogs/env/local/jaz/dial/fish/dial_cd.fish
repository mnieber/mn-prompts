# managed by zoo dial.install-fish
function dial_cd --description 'cd to the directory of dial key $argv[2] in group $argv[1]'
    type -q zoo; or return
    set -l dir (zoo dial.get $argv[2] group=$argv[1] dir=true)
    # A bare cd would go to the home directory
    if test -n "$dir"
        cd "$dir"
    end
    commandline -f repaint
end
