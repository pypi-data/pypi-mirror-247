
1. To install dependency
    * `pip install mkdocs mkdocstrings-python==1.3.0`

2. Run in local
    * `mkdocs serve` [under the src dir where mkdocs.yml located]

    2.1 Run in local on specific port
        * `mkdocs serve -a localhost:8001` [under the src dir where mkdocs.yml located]

3. Pull (others will change the other readthedocs files)
    * cd .../virtuousai.bi...;
    * git pull

4. Making Build
    * `mkdocs build` [under the mkdocs dir] e.g.,
    <!-- * mv vai-toolkit/readthedocs/build/* virtuousai.bitbucket.io/docs/vai-toolkit/  This will not work as strcture changed  -->

5. Uploading Build
    * `mkdocs build will generate build folder, copy all content in other repo in respective folder and push there`
