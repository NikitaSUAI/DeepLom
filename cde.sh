cde()
{
        if [ "$1" == "-e" ]; then
                if [ -d "$PWD/env" ]; then
                        echo "Goodbue";
                        deactivate;
                        return
                fi
        fi
        if [ "$1" = "-r" ]; then
                if [ -d "$PWD/env" ]; then
                        deactivate;
                        source env/bin/activate;
                        echo "Reactivate";
                        return
                fi
        fi
        if [ "$1" = ".." ]; then
                if [ -d "$PWD/env" ]; then
                        deactivate;
                        echo "Goodbye";
                fi
        fi
        cd "$1"
        if [ -d "$PWD/env" ]; then
                source env/bin/activate;
                echo "Hello";
        fi;
}
