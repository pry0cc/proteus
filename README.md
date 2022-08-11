this is the branch for the pdiscovery-bot! 

https://blog.projectdiscovery.io/asm-platform-using-projectdiscovery-tools/

To run use the following commands:
```
cd ./bin
pip3 install -r requirements.txt
sh ./start_db.sh
flask run
streamlit run ./bin/ui.py
python3 worker.py 
```
Results can be viewed with the simple UI utilising streamlit.

<img width="1069" alt="image" src="https://user-images.githubusercontent.com/954507/184242099-64a426cc-a224-4187-8e0e-3e02729b97bd.png">
