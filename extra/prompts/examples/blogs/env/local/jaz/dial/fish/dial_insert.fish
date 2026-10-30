# managed by zoo dial.install-fish
function dial_insert --description 'Insert the value of dial key $argv[1] (group default) in the command line'
    type -q zoo; or return
    set -l value (zoo dial.get $argv[1])
    if test -n "$value"
        commandline -i -- "$value"
    end
    commandline -f repaint
end
