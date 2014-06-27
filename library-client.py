# We import the graphics library GTK, because we want to make a graphical interface that is cross-platform and looks modern.

from gi.repository import Gtk, GObject

# We import sqlite, to work with the database file.

import sqlite3

# We import os, to use it for filepaths

import os


class database:
  """API for the User Interface to interact with the SQLite database."""
  # We open the database at initialization so it can be interacted with
  def __init__(self):
    self.dbpath = os.path.join('data','books.sqlite')
    self.db = sqlite3.connect(self.dbpath)
    self.cursor = self.db.cursor()

  def TitleSearch(self,title):
    """Search the book database by title."""
    self.cursor.execute("select * from books where title like ?;",[("%" + title + "%")])

  def AuthorSearch(self,author):
    """Search the book database by author."""
    self.cursor.execute("select * from books where author like ?;",[("%" + author + "%")])

  def SubjectSearch(self,subject):
    """Search the book database by subject category."""
    self.cursor.execute("select * from books where title like ? or summary like ? or subjects like ?", [("%" + subject + "%"),("%" + subject + "%"),("%" + subject + "%")])

  def FlipAvailability(self,index):
    """Flip the availability boolean of a given book record. (Not Yet Implemented)"""

  def Results(self):
    """Return the results from the last search query."""
    return self.cursor.fetchall()

class interface(Gtk.Window):
  """API for the Database to interact with the User Interface."""
  # We draw a window and open the inital search interface
  def __init__(self):
    Gtk.Window.__init__(self,title="A&T Library Search")
    self.set_size_request(400,200)
    self.SearchView()

  def SearchView(self):
    """Draw the initial search view which the user will make their first book search from."""
    self.SearchViewbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
    self.add(self.SearchViewbox)    

    self.SearchBox = Gtk.Box(spacing=0)
    self.SearchSelect = Gtk.ComboBoxText()
    self.SearchSelect.insert(0,"title","Title:")
    self.SearchSelect.insert(1,"author","Author:")
    self.SearchSelect.insert(2,"subject","Subject:")
    self.SearchSelect.set_active(0)
    self.SearchBox.pack_start(self.SearchSelect,False,True,0)
    
    self.SearchBar = Gtk.Entry()
    self.SearchBar.connect("activate", self._Query)
    self.SearchBox.pack_start(self.SearchBar,True,True,0)
    self.SearchViewbox.add(self.SearchBox)

  def ResultsView(self,results):
    """Add the results list to the SearchView."""
    self.ResultsList = Gtk.ListStore(str,str)
    for result in results:
      self.ResultsList.append([result[1],result[2]])

    self.ResultsListView = Gtk.TreeView(model=self.ResultsList)
    
    self.Column_Renderer_One = Gtk.CellRendererText()
    self.Column_Renderer_Two = Gtk.CellRendererText()

    self.Column_One = Gtk.TreeViewColumn("Title:", self.Column_Renderer_One, text=0)
    self.Column_Two = Gtk.TreeViewColumn("Author:", self.Column_Renderer_Two, text=1)

    self.ResultsListView.append_column(self.Column_One)
    self.ResultsListView.append_column(self.Column_Two)

    self.SearchViewbox.add(self.ResultsListView)
    self.show_all()

  def BookView(self):
    """Format a single book record from results and display it to the user."""

  def _Query(self,button):
    """Perform the query from the search view and obtain the results."""
    self.QueryText = self.SearchBar.get_text()
    if self.SearchSelect.get_active_id() == "title":
      db.TitleSearch(self.QueryText)
    if self.SearchSelect.get_active_id() == "author":
      db.AuthorSearch(self.QueryText)
    if self.SearchSelect.get_active_id() == "subject":
      db.SubjectSearch(self.QueryText)
    else:
      None
    self.ResultsView(db.Results())

db = database()

window = interface()
window.connect("delete-event",Gtk.main_quit)
window.show_all()
Gtk.main()
