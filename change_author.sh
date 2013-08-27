#for dir in $(find ./ -type d); do
git filter-branch --commit-filter '
        if [ "$GIT_COMMITTER_NAME" = "Tim de Jager" ];
        then
                GIT_COMMITTER_NAME="Tim de Jager";
                GIT_AUTHOR_NAME="Tim de Jager";
                GIT_COMMITTER_EMAIL="tdejager89@gmail.com";
                GIT_AUTHOR_EMAIL="tdejager89@gmail.com";
                git commit-tree "$@";
        else
                git commit-tree "$@";
        fi' HEAD
git pull origin master
git push origin master
#done
