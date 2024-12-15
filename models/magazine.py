from database.connection import get_db_connection
class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
       return f'<Magazine {self.id} {self.name} {self.category}>'
    
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        if isinstance(id,int):
            self._id = id
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and 2 <= len(new_name) <= 16:
            self._name = new_name
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, new_category):
        if isinstance(new_category, str) and len(new_category) > 0:
            self._category = new_category
    def save(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            INSERT INTO magazines(name,category)
            VALUES (?,?)
        """
        CURSOR.execute(sql,(self.name,self.category))
        conn.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
    @classmethod
    def create(cls, name, category):
        magazine = cls( name, category)
        magazine.save()
        return magazine
    
    def get_magazine_id(self):
        return self.id
    
    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT ar.* 
            FROM articles ar 
            INNER JOIN magazines m ON ar.magazines = m.id
            WHERE magazine_id = ?
        """
        CURSOR.execute(sql,(self.id,))
        articles_data = CURSOR.fetchall()
        article = []
        for article_data in articles_data:
            article.append(Article(*article_data))
        return article
    
    def contributors(self):
        from models.author import Author
        conn = get_db_connection()
        CURSOR = conn.cursor()
        """retrieves and returns a lst of authors who wrote articles in this magazine"""
        sql = """
            SELECT DISTINCT a.*
            FROM authors a
            INNER JOIN articles ar ON ar.author = a.id
            INNER JOIN magazines m on ar.magazine = m.id
            WHERE m.id = ?
        """
        CURSOR.execute(sql, (self.id,))
        author_data = CURSOR.fetchall()
        authors = []
        for row in author_data:
            authors.append(Author(*row))
        return authors
    def article_titles(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT ar.title
            FROM articles ar
            INNER JOIN magazines m ON ar.magazine = m.id
            WHERE m.id = ?
        """
        CURSOR.execute(sql, (self.id,))
        article_data = CURSOR.fetchall()
        if not article_data:
            return None
        titles = [row[0] for row in article_data]
        return titles
    def contributing_authors(self):
        from models.author import Author
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT DISTINCT a.*
            FROM authors a
            INNER JOIN articles ar ON ar.author = a.id
            INNER JOIN magazines m on ar.magazine = m.id
            WHERE m.id = ?
            GROUP BY a.id
            HAVING COUNT(ar.id) > 2
        """
        CURSOR.execute(sql, (self.id,))
        author_data = CURSOR.fetchall()
        if not author_data:
            return None
        authors = []
        for row in author_data:
            authors.append(Author(*row)) 
        return authors
    
    @classmethod
    def find_by_id(cls, id):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT * FROM magazines
            WHERE id = ?
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return Magazine(*row)
        return None
