if [ "$#" -eq 1 ]
then
    python Proofreader/readme_dfs.py $1
else
    python Proofreader/readme_dfs.py
fi

echo 'CHECK!! -> https://competent-morse-3888be.netlify.app/'
