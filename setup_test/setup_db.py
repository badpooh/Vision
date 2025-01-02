import sqlite3

class IPDataBase:
  def __init__(self, db_path='ip_data.db'):
    self.conn = sqlite3.connect(db_path)
    self.create_table()
    
  def create_table(self):
    # ip_addresses 테이블이 없으면 생성
    self.conn.execute('''
        CREATE TABLE IF NOT EXISTS ip_addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            touch_port TEXT NOT NULL,
            setup_port TEXT NOT NULL
        );
    ''')
    self.conn.commit()
        
  def add_ip(self, ip_text):
    self.conn.execute('INSERT INTO ip_addresses (ip) VALUES (?)', (ip_text,))
    self.conn.commit()
    
  def add_touch_port(self, tp_text):
    self.conn.execute('INSERT INTO ip_addresses (touch_port) VALUES (?)', (tp_text,))
    self.conn.commit()
  
  def add_setup_port(self, sp_text):
    self.conn.execute('INSERT INTO ip_addresses (setup_port) VALUES (?)', (sp_text,))
    self.conn.commit()

  def get_all_ips(self):
    cursor = self.conn.execute('SELECT id, ip, touch_port, setup_port FROM ip_addresses')
    return cursor.fetchall()

  def delete_ip(self, ip_text):
    self.conn.execute('DELETE FROM ip_addresses WHERE ip = ?', (ip_text,))
    self.conn.commit()
    
  def delete_tp(self, tp_text):
    self.conn.execute('DELETE FROM ip_addresses WHERE touch_port = ?', (tp_text,))
    self.conn.commit()

  def delete_sp(self, sp_text):
    self.conn.execute('DELETE FROM ip_addresses WHERE setup_port = ?', (sp_text,))
    self.conn.commit()

