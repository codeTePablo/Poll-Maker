# Poll-Maker

![GitHub repo size](https://img.shields.io/github/repo-size/codeTePablo/Poll-Maker)
![GitHub contributors](https://img.shields.io/github/contributors/codeTePablo/Poll-Maker)
![GitHub stars](https://img.shields.io/github/stars/codeTePablo/Poll-Maker?style=social)

**Poll Maker is a free database using ElephantSQL to store polls and graph them.**

- ElephantSQL is a PostgreSQL database hosting service. ElephantSQL will manage administrative tasks of PostgreSQL, such as installation, upgrades to latest stable version and backup handling.
    
    - To use the database you must have an account (free plan), create a new instance that will give you a URL like this: : 
        ```
        postgres://dvdugkio:NAJhdjanNNajfjkkonQjdfr-h@mahmud.db.elephantsql.com/fsajfkla
        ```
- Caution: anyone who has your URI can access to create, vote, delete, etc. within your database.  

## Installing Poll Maker

To setup Poll Maker, follow these step:
```
pip install -r requirements.txt
```
## Using Poll Maker

To use Poll Maker, follow these steps:

* Create file called:
        ```
        .env
        ```
    
    Inside this file you will put the URL you generated before. 
    ```
    DATABASE_URI=postgres://dvdugkio:NAJhdjanNNajfjkkonQjdfr-h@mahmud.db.elephantsql.com/fsajfkla
    ```

Now you can run

```
py main.py
```

### Transactions
After running [main.py](https://cirosantiilli.com/markdown-style-guide) you will find in this menu:

[![menu.png](https://i.postimg.cc/tgXk7x5N/menu.png)](https://postimg.cc/TK4g4hBK)

- we created some polls:

- [![list-polls.png](https://i.postimg.cc/6pVz90dQ/list-polls.png)](https://postimg.cc/216nGn9p)

After adding some votes, we can **view the graphs**. 

- [![pie-chart.png](https://i.postimg.cc/QM0b7dYG/pie-chart.png)](https://postimg.cc/bGSkcpj3)
- [![pie-chart-2.png](https://i.postimg.cc/gJjKHb1w/pie-chart-2.png)](https://postimg.cc/JDwJRvrm)
- [![all-polls.png](https://i.postimg.cc/3xQn5606/all-polls.png)](https://postimg.cc/Vd4jXKRB)

Also, we can check in what moment someone vote on someone poll.

- [![time.png](https://i.postimg.cc/rmHNhYLf/time.png)](https://postimg.cc/WFMZz8zZ)

### Documentation

##### Entity Relation Model
[![ERM.png](https://i.postimg.cc/L8MHGJ7t/ERM.png)](https://postimg.cc/3dn5vx3N)
