import wx
from DBController import DBConnection
import cx_Oracle

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"DBInterface", pos=wx.DefaultPosition,
                          size=wx.Size(1000, 665), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL, name=u"DBInterface")

        self.initVisualElements()
        self.connectToDB()

    def initVisualElements(self):
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainVSizer = wx.BoxSizer(wx.VERTICAL)

        self.mainNotebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.tableDisplayPage = wx.Panel(self.mainNotebook, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1),
                                         wx.TAB_TRAVERSAL)
        tableDisplayVSizer = wx.BoxSizer(wx.VERTICAL)

        searchHSizer = wx.BoxSizer(wx.HORIZONTAL)

        searchLabelVSizer = wx.BoxSizer(wx.VERTICAL)

        self.columnSearchLabel = wx.StaticText(self.tableDisplayPage, wx.ID_ANY, u"Fields", wx.DefaultPosition,
                                               wx.DefaultSize, wx.ALIGN_LEFT)
        self.columnSearchLabel.Wrap(-1)
        searchLabelVSizer.Add(self.columnSearchLabel, 0, wx.BOTTOM | wx.LEFT | wx.TOP, 11)

        self.filterSearchLabel = wx.StaticText(self.tableDisplayPage, wx.ID_ANY, u"Filters", wx.DefaultPosition,
                                               wx.DefaultSize, wx.ALIGN_LEFT)
        self.filterSearchLabel.Wrap(-1)
        searchLabelVSizer.Add(self.filterSearchLabel, 0, wx.BOTTOM | wx.LEFT | wx.TOP, 11)

        searchHSizer.Add(searchLabelVSizer, 0, wx.ALIGN_LEFT | wx.ALIGN_TOP, 5)

        searchFiendVSizer = wx.BoxSizer(wx.VERTICAL)

        self.columnSearchField = wx.TextCtrl(self.tableDisplayPage, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.Size(400, -1), 0)
        searchFiendVSizer.Add(self.columnSearchField, 0, wx.ALL, 8)

        self.filterSearchField = wx.TextCtrl(self.tableDisplayPage, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.Size(400, -1), 0)
        searchFiendVSizer.Add(self.filterSearchField, 0, wx.ALL, 8)

        searchHSizer.Add(searchFiendVSizer, 0, wx.ALIGN_RIGHT | wx.ALIGN_TOP, 5)

        tableVSizer = wx.BoxSizer(wx.VERTICAL)

        tableRadioBoxChoices = [u"Users", u"Items"]
        self.tableRadioBox = wx.RadioBox(self.tableDisplayPage, wx.ID_ANY, u"Table", wx.DefaultPosition, wx.DefaultSize,
                                         tableRadioBoxChoices, 1, wx.RA_SPECIFY_COLS)
        self.tableRadioBox.SetSelection(0)
        tableVSizer.Add(self.tableRadioBox, 0, wx.ALL, 0)

        searchHSizer.Add(tableVSizer, 0, 0, 0)

        searchButtonVSizer = wx.BoxSizer(wx.VERTICAL)

        self.searchButton = wx.Button(self.tableDisplayPage, wx.ID_ANY, u"Search", wx.DefaultPosition, wx.DefaultSize,
                                      0)
        searchButtonVSizer.Add(self.searchButton, 1, wx.ALIGN_BOTTOM | wx.ALL, 5)

        searchHSizer.Add(searchButtonVSizer, 1, wx.ALIGN_BOTTOM, 5)

        pageButtonHSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.prevPageButton = wx.Button(self.tableDisplayPage, wx.ID_ANY, u"<", wx.DefaultPosition, wx.DefaultSize, 0)
        pageButtonHSizer.Add(self.prevPageButton, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

        self.nextPageButton = wx.Button(self.tableDisplayPage, wx.ID_ANY, u">", wx.DefaultPosition, wx.DefaultSize, 0)
        pageButtonHSizer.Add(self.nextPageButton, 0, wx.ALL, 5)

        searchHSizer.Add(pageButtonHSizer, 0, wx.ALIGN_BOTTOM, 5)

        tableDisplayVSizer.Add(searchHSizer, 0, wx.EXPAND, 5)

        self.resultList = wx.ListCtrl(self.tableDisplayPage, wx.ID_ANY, wx.DefaultPosition, wx.Size(300, 300),
                                      wx.LC_REPORT)
        tableDisplayVSizer.Add(self.resultList, 1, wx.ALL | wx.EXPAND, 5)

        self.tableDisplayPage.SetSizer(tableDisplayVSizer)
        self.tableDisplayPage.Layout()
        tableDisplayVSizer.Fit(self.tableDisplayPage)
        self.mainNotebook.AddPage(self.tableDisplayPage, u"Tables", True)
        self.MiscPage = wx.Panel(self.mainNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        miscVSizer = wx.BoxSizer(wx.VERTICAL)

        self.CRUDLabel = wx.StaticText(self.MiscPage, wx.ID_ANY, u"CRUD Operations", wx.DefaultPosition, wx.DefaultSize,
                                       0)
        self.CRUDLabel.Wrap(-1)
        miscVSizer.Add(self.CRUDLabel, 0, wx.ALL, 5)

        CRUDHSizer = wx.BoxSizer(wx.HORIZONTAL)

        crudOpRadioBoxChoices = [u"Create(Insert)", u"Update", u"Delete(ID based)"]
        self.crudOpRadioBox = wx.RadioBox(self.MiscPage, wx.ID_ANY, u"Operation", wx.DefaultPosition, wx.DefaultSize,
                                          crudOpRadioBoxChoices, 1, wx.RA_SPECIFY_COLS)
        self.crudOpRadioBox.SetSelection(1)
        CRUDHSizer.Add(self.crudOpRadioBox, 0, wx.ALL, 5)

        crudTableRadioBoxChoices = [u"Users", u"Items"]
        self.crudTableRadioBox = wx.RadioBox(self.MiscPage, wx.ID_ANY, u"On Table", wx.DefaultPosition, wx.DefaultSize,
                                             crudTableRadioBoxChoices, 1, wx.RA_SPECIFY_COLS)
        self.crudTableRadioBox.SetSelection(0)
        CRUDHSizer.Add(self.crudTableRadioBox, 0, wx.ALL, 5)

        crudTextFieldsVSizer = wx.BoxSizer(wx.VERTICAL)

        self.crudColumnsLabel = wx.StaticText(self.MiscPage, wx.ID_ANY, u"Columns", wx.DefaultPosition, wx.DefaultSize,
                                              0)
        self.crudColumnsLabel.Wrap(-1)
        crudTextFieldsVSizer.Add(self.crudColumnsLabel, 0, wx.TOP | wx.LEFT, 5)

        self.crudColumnField = wx.TextCtrl(self.MiscPage, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.Size(400, -1), 0)
        crudTextFieldsVSizer.Add(self.crudColumnField, 0, wx.LEFT, 5)

        self.crudValuesLabel = wx.StaticText(self.MiscPage, wx.ID_ANY, u"Values", wx.DefaultPosition, wx.DefaultSize, 0)
        self.crudValuesLabel.Wrap(-1)
        crudTextFieldsVSizer.Add(self.crudValuesLabel, 0, wx.TOP | wx.LEFT, 5)

        self.crudValuesField = wx.TextCtrl(self.MiscPage, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(400, -1),
                                           0)
        crudTextFieldsVSizer.Add(self.crudValuesField, 0, wx.LEFT, 5)

        self.crudFiltersLabel = wx.StaticText(self.MiscPage, wx.ID_ANY, u"Where(Filters)", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.crudFiltersLabel.Wrap(-1)
        crudTextFieldsVSizer.Add(self.crudFiltersLabel, 0, wx.ALL, 5)

        self.crudFiltersField = wx.TextCtrl(self.MiscPage, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                            wx.Size(400, -1), 0)
        crudTextFieldsVSizer.Add(self.crudFiltersField, 0, wx.ALL, 5)

        CRUDHSizer.Add(crudTextFieldsVSizer, 0, wx.EXPAND, 5)

        self.crudExecuteButton = wx.Button(self.MiscPage, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.Size(60, 50), 0)
        CRUDHSizer.Add(self.crudExecuteButton, 0, wx.ALIGN_CENTER | wx.ALIGN_LEFT | wx.ALL, 25)

        miscVSizer.Add(CRUDHSizer, 0, wx.EXPAND, 5)

        dbFuncHsizer = wx.BoxSizer(wx.HORIZONTAL)

        self.cleaUpDBButton = wx.Button(self.MiscPage, wx.ID_ANY, u"Old Item Cleanup", wx.DefaultPosition,
                                        wx.Size(-1, 50), 0)
        dbFuncHsizer.Add(self.cleaUpDBButton, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button7 = wx.Button(self.MiscPage, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0)
        dbFuncHsizer.Add(self.m_button7, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button8 = wx.Button(self.MiscPage, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0)
        dbFuncHsizer.Add(self.m_button8, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        miscVSizer.Add(dbFuncHsizer, 1, 0, 20)

        self.MiscPage.SetSizer(miscVSizer)
        self.MiscPage.Layout()
        miscVSizer.Fit(self.MiscPage)
        self.mainNotebook.AddPage(self.MiscPage, u"Misc", False)

        mainVSizer.Add(self.mainNotebook, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(mainVSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.searchButton.Bind(wx.EVT_BUTTON, self.onSearch)
        self.prevPageButton.Bind(wx.EVT_BUTTON, self.onPrevPage)
        self.nextPageButton.Bind(wx.EVT_BUTTON, self.onNextPage)
        self.crudExecuteButton.Bind(wx.EVT_BUTTON, self.onCrudExecute)
        self.cleaUpDBButton.Bind(wx.EVT_BUTTON, self.onDBCleanup)
    def connectToDB(self):
        self.dbConnection = DBConnection.connect("PROJECT1", "project1", "localhost")



    def onSearch(self, event):

        command = self.composeSelectComand()

        if self.executeSelectCommand(command) == False:
            return

        self.initializeResultListColumns()

        self.getSelectResultPages(25)

        self.displayResultPage(0)

    def initializeResultListColumns(self):
        self.resultList.DeleteAllColumns()
        self.resultList.DeleteAllItems()

        columnIndex = 1
        columns = str(self.columnSearchField.GetValue()).replace(" ", "").split(",")
        self.resultList.InsertColumn(0, "#")
        for column in columns:
            self.resultList.InsertColumn(columnIndex, column.capitalize())
            columnIndex += 1
    def composeSelectComand(self):
        SQL_select  = "select "                                         # SELECT
        SQL_columns = str(self.columnSearchField.GetValue())            # COLUMNS
        SQL_from    = " from "                                          # FROM

        if self.tableRadioBox.GetSelection() == 0:                      # TABLE
            SQL_table = "site_users"
        else:
            SQL_table = "items"

        if len(str(self.filterSearchField.GetValue())) > 1:             # WHERE
            SQL_where      = " where "
            SQL_conditions =  str(self.filterSearchField.GetValue())    # CONDITIONS
        else:
            SQL_where      = ""
            SQL_conditions = ""

        return SQL_select + SQL_columns + SQL_from + SQL_table + SQL_where + SQL_conditions
    def executeSelectCommand(self, command):
        selectResult = self.dbConnection.execute(command)
        if type(selectResult) == str and str(selectResult).startswith("E"):
            self.onError(selectResult)
            return False
        else:
            return True
    def getSelectResultPages(self, pageSize):
        self.currentPage = 0
        self.resultPages = []
        for page in self.dbConnection.getResultsInPagesOf(pageSize):
            resultPage = []

            for entry in page:
                resultEntry = []

                for field in entry:
                    resultEntry.append(str(entry))

                resultPage.append(entry)

            self.resultPages.append(resultPage)
    def displayResultPage(self, pageNumber):
        self.resultList.DeleteAllItems()

        rowIndex = 0
        for result in self.resultPages[pageNumber]:
            self.resultList.InsertStringItem(rowIndex, str(rowIndex + 1))
            fieldIndex = 1
            for field in result:
                self.resultList.SetStringItem(rowIndex, fieldIndex, str(field))
                fieldIndex += 1
            rowIndex += 1



    def onPrevPage(self, event):
        if self.currentPage == 0:
            event.Skip()
        else:
            self.currentPage -= 1
            self.displayResultPage(self.currentPage)
    def onNextPage(self, event):
        if self.currentPage == len(self.resultPages) - 1:
            event.Skip()
        else:
            self.currentPage += 1
            self.displayResultPage(self.currentPage)



    def onCrudExecute(self, event):

        if self.crudOpRadioBox.GetSelection() == 0: # INSERT
            self.onInsert()
            return True

        if self.crudOpRadioBox.GetSelection() == 2:  # DELETE
            self.onDelete()
            return True

        if self.crudOpRadioBox.GetSelection() == 1: # UPDATE
            self.onUpdate()
            return True



    def onDelete(self):
        if self.crudTableRadioBox.GetSelection() == 0:  # USERS
            Id = int(str(self.crudFiltersField.GetValue()))
            userId = [Id]

            deleteResult = self.dbConnection.callProcedure("DELETE_USER", userId)
            if type(deleteResult) == str and str(deleteResult).startswith("E"):
                self.onError(deleteResult)
                return False
            else:
                crudCommandDialog = wx.MessageDialog(self, "CRUD Delete operation completed.", "Done", wx.OK,
                                                     (350, 300))
                crudCommandDialog.ShowModal()
                return True

        if self.crudTableRadioBox.GetSelection() == 1:  # ITEMS
            Id = int(str(self.crudFiltersField.GetValue()))
            itemId = [Id]

            deleteResult = self.dbConnection.callProcedure("DELETE_ITEM", itemId)
            if type(deleteResult) == str and str(deleteResult).startswith("E"):
                self.onError(deleteResult)
                return False
            else:
                crudCommandDialog = wx.MessageDialog(self, "CRUD Delete operation completed.", "Done", wx.OK,
                                                     (350, 300))
                crudCommandDialog.ShowModal()
                return True
    def onInsert(self):
        if self.crudTableRadioBox.GetSelection() == 0: # USERS
            newUserData = str(self.crudValuesField.GetValue()).split(",")

            insertResult = self.dbConnection.callProcedure("ADD_USER", newUserData)
            print insertResult
            if type(insertResult) == str and str(insertResult).startswith("E"):
                self.onError(insertResult)
                return False
            else:
                crudCommandDialog = wx.MessageDialog(self, "CRUD Insert operation completed.", "Done", wx.OK, (350, 300))
                crudCommandDialog.ShowModal()
                return True

        if self.crudTableRadioBox.GetSelection() == 1:  # ITEMS
            newItemData = str(self.crudValuesField.GetValue()).split(",")

            insertResult = self.dbConnection.callProcedure("ADD_ITEM", newItemData)
            if type(insertResult) == str and str(insertResult).startswith("E"):
                self.onError(insertResult)
                return False
            else:
                crudCommandDialog = wx.MessageDialog(self, "CRUD Insert operation completed.", "Done", wx.OK, (350, 300))
                crudCommandDialog.ShowModal()
                return True
    def onUpdate(self):
        if self.crudTableRadioBox.GetSelection() == 0: # USERS
            newUserData = str(self.crudValuesField.GetValue()).split(",")

            updateResult = self.dbConnection.callProcedure("UPDATE_USER", newUserData)
            print updateResult
            if type(updateResult) == str and str(updateResult).startswith("E"):
                self.onError(updateResult)
                return False
            else:
                crudCommandDialog = wx.MessageDialog(self, "CRUD Update operation completed.", "Done", wx.OK,
                                                     (350, 300))
                crudCommandDialog.ShowModal()
                return True







    def composeCrudCommand(self):

        command = "Invalid"

        if self.crudOpRadioBox.GetSelection() == 0: # CREATE(Insert)
            command = self.composeInsert()

        if self.crudOpRadioBox.GetSelection() == 1: # UPDATE
            command = self.composeUpdate()


            if command == False:
                self.onError("Invalid DELETE filters")

        print command

    def onDBCleanup(self, event):
        archivedItems = 0
        parameterList = [archivedItems]
        parameterList = self.dbConnection.callProcedure("CLEANUP_OLD_ITEMS", parameterList)

        print "Archived Items: ", parameterList[0]

        archivedItemsDialog = wx.MessageDialog(self, str("Archived " + str(parameterList[0]) + " items."), "Archiving Complete", wx.OK, (350, 300))
        archivedItemsDialog.ShowModal()


    def onError(self, errorText):
        errorDialog = wx.MessageDialog(self, errorText, "Error", wx.OK, (300, 300))
        errorDialog.ShowModal()
