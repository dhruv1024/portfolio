############
# Pending
############
# Add Requirements files for all projects and ensure they work on download
# Add description for all projects

############
# Git Commit
############
# Git commands
echo "# portfolio" >> README.md

git init

git add README.md

git commit -m "first commit"

git branch -M main

git remote add origin https://github.com/dhruv1024/portfolio.git

git push -u origin main
