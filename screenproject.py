import os
import configparser
import shutil
import sqlite3
import tempfile
from kivy.uix.popup import Popup
from kivy.app import App 
from kivy.config import ConfigParser
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from generalelements import NormalPopup, ConfirmPopup, MoveConfirmPopup,MenuButton, ScanningPopup, InputPopup, InputPopupTag, MenuButton, NormalDropDown, AlbumSortDropDown, AlbumExportDropDown
Builder.load_string("""
<ProjectScreen>:
    name: "project_screen"
    canvas.before:
        Color:
            rgba: app.theme.background
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: app.theme.main_background
        Rectangle:
            size: self.size
            pos: self.pos
            source: 'data/mainbg.png'

    BoxLayout:
        orientation: 'vertical'

        MainHeader:
            NormalButton:
                text: 'Back'
                on_release: app.show_menu()
            HeaderLabel:
                text: "Project Manager"
                halign: 'center'
                valign: 'middle'
                size_hint_y: None
                height: app.button_scale

        FloatLayout:
            BoxLayout:
                orientation: 'vertical'
                spacing: dp(20)
                size_hint: None, None
                width: min(root.width * 0.8, dp(400))
                height: self.minimum_height
                pos_hint: {"center_x": 0.5, "center_y": 0.5}

                # Create New Project Section
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    canvas.before:
                        Color:
                            rgba: app.theme.area_background
                        BorderImage:
                            pos: self.pos
                            size: self.size
                            source: 'data/buttonflat.png'
                    padding: dp(10)

                    NormalLabel:
                        text: "Create New Project:"
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: dp(40)

                        NormalInput:
                            id: new_project_name
                            multiline: False
                            disable_lines: True
                            hint_text: 'Project Name'
                            on_text: ok_button.disabled = root.project_name_exists(self.text)
                            height: dp(40)
                        NormalButton:
                            id: ok_button
                            text: 'Ok'
                            on_release: root.create_project_folder(new_project_name.text)
                            size_hint_y: None
                            height: dp(40)

                # Select Project Section
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    canvas.before:
                        Color:
                            rgba: app.theme.area_background
                        BorderImage:
                            pos: self.pos
                            size: self.size
                            source: 'data/buttonflat.png'
                    padding: dp(10)

                    NormalLabel:
                        text: "Select Project"

                    MenuStarterButtonWide:
                        id: project_button
                        text: 'Select Current Project'
                        size_hint_y: None
                        height: dp(44)
                        on_release: root.open_project_dropdown(self)

                # Launch Project Section
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    canvas.before:
                        Color:
                            rgba: app.theme.area_background
                        BorderImage:
                            pos: self.pos
                            size: self.size
                            source: 'data/buttonflat.png'
                    padding: dp(10)

                    NormalLabel:
                        text: "Launch The Selected Project"
                    
                    WideButton:
                        id: launch_button
                        text: 'Launch Project'
                        on_release: root.launch_project()
                        size_hint_y: None
                        height: dp(40)

                # Delete Project Section
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    canvas.before:
                        Color:
                            rgba: app.theme.area_background
                        BorderImage:
                            pos: self.pos
                            size: self.size
                            source: 'data/buttonflat.png'
                    padding: dp(10)

                    NormalLabel:
                        text: "Delete The Selected Project"
                    
                    DeleteButton:
                        id: delete_button
                        padding: dp(20)
                        spacing: dp(20)
                        text: 'Delete Project'
                        color: (0, 0, 0, 1)                       
                        height: dp(40)
                        disabled: True
                        on_release: root.delete_selected_project()
     
                        canvas.before:
                            Color:
                                rgba: 0, 0, 0, 0.2  # Shadow color
                            RoundedRectangle:
                                pos: self.x, self.y - dp(2)
                                size: self.size
                                radius: [20]

                            Color:
                                rgba: self.background_color
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [20]

""")




class ProjectScreen(Screen):
    def create_project_folder(self, folder_name):
        """Creates a folder in the AppData Roaming directory"""
        app = App.get_running_app()
        if not folder_name.strip():
            return 
        folder_name = folder_name.lower() 
        appdata_path = os.path.join(os.getenv('APPDATA'), 'snu photo manager', folder_name)
        
        if os.path.exists(appdata_path):
            print(f"Folder '{folder_name}' already exists!")
            return 
        
        try:
            os.makedirs(appdata_path, exist_ok=True)
            print(f"Folder created at: {appdata_path}")  
            
            # app.config.set('Project', 'name', folder_name)
            # app.config.write()
            
            # app.project_name = folder_name
            # self.data_directory = appdata_path 
            app.setup_directories(appdata_path)
            project_config_file = app.get_application_config(folder_name)
            config = ConfigParser()
        
        # Load project-specific config file
            if os.path.exists(project_config_file):
                config.read(project_config_file)

            # Ensure 'Project' section exists
            if not config.has_section('Project'):
                config.add_section('Project')

            # Set project name in the correct config file
            config.set('Project', 'name', folder_name)
            config.write()
                        # app.config.set('Project', 'name', folder_name)
            # app.config.write()
            # if hasattr(app, 'setup_directories'):
            #     app.setup_directories(appdata_path)  # Pass the created folder path
            # else:
            #     print("Error: app.setup_directories() method is missing!")
            self.ids.new_project_name.text = ""
        except Exception as e:
            print(f"Error creating folder: {e}") 
            
    def project_name_exists(self, folder_name):
        """Returns True if the project folder already exists."""
        if not folder_name.strip():
            return False  
        
        folder_name = folder_name.lower()
        appdata_path = os.path.join(os.getenv('APPDATA'), 'snu photo manager', folder_name)
        
        return os.path.exists(appdata_path)
            
    def open_project_dropdown(self,instance=None):
        """Creates a dropdown menu with available projects."""
        app = App.get_running_app()
        dropdown = NormalDropDown() 

        available_projects = app.get_available_projects() 
        selected_project = self.ids.project_button.text 
        available_projects = [project for project in available_projects if project != selected_project]

        if not available_projects:
            btn = Button(text="No projects found", size_hint_y=None, height=44)
            dropdown.add_widget(btn)
        else:
            for project in available_projects:
                btn = MenuButton(text=project, size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn=btn: self.select_project(btn.text, dropdown))
                dropdown.add_widget(btn)

        dropdown.open(instance)
        
    def select_project(self, project_name, dropdown):
        """Handles project selection from the dropdown."""
        self.ids.project_button.text = project_name 
        app = App.get_running_app()
        app.load_project_config(project_name) 
        self.ids.delete_button.disabled = False

        dropdown.dismiss()
        
    def launch_project(self):
        """Launches the selected project and opens the DatabaseScreen."""
        app = App.get_running_app()
        selected_project = self.ids.project_button.text 


        if not selected_project or selected_project in ["Default_project", "Select Current Project"]:
            print("[WARNING] No valid project selected to launch!")
            return    
        app.selected_project = selected_project

        
        app.load_project_config(selected_project)

        app.screen_manager.current = 'database'
        
        selected_project = selected_project.lower() 
        appdata_path = os.path.join(os.getenv('APPDATA'), 'snu photo manager', selected_project)

        app.setup_directories(appdata_path)
        app.refresh_database_screen()
        # app.show_database(selected_project)

        print(f"[INFO] Launched project: {selected_project}")
        
    def some_database_operation(self):
        app = App.get_running_app()
        conn = app.get_db_connection(app.selected_project)
        cursor = conn.cursor()
        # Perform database operations
        cursor.close() 
           
    def delete_selected_project(self):
        app = App.get_running_app()
        selected_project = self.ids.project_button.text.strip()

        if not selected_project or selected_project in ["Default_project", "Select Current Project"]:
            print("[WARNING] No valid project selected to delete!")
            return

        # Construct paths
        config_dir = app.get_project_config_directory()
        ini_path = os.path.join(config_dir, f"{selected_project}.ini")
        project_folder = os.path.join(os.getenv('APPDATA'), 'snu photo manager', selected_project.lower())

        # Confirmation popup
        def confirm_deletion(instance):
            try:
                print(f"[DEBUG] Attempting to delete: {project_folder}")

                # Close the database if it's open for this project
                if getattr(app, "selected_project", None) == selected_project:
                    app.close_database()
                    print("[DEBUG] Database connection closed")

                # Ensure all database files are closed
                db_folder = os.path.join(project_folder, "Databases")
                if os.path.exists(db_folder):
                    for root, dirs, files in os.walk(db_folder):
                        for file in files:
                            if file.endswith(".db"):
                                db_path = os.path.join(root, file)
                                try:
                                    os.chmod(db_path, 0o777)  # Change permissions to ensure access
                                    with open(db_path, 'r+'):  # Open and close the file to release locks
                                        pass
                                except Exception as e:
                                    print(f"[WARNING] Could not release lock for {db_path}: {e}")

                # Remove ini file
                if os.path.exists(ini_path):
                    os.remove(ini_path)
                    print(f"[INFO] Deleted .ini file: {ini_path}")

                # Delete the project folder
                if os.path.exists(project_folder):
                    shutil.rmtree(project_folder)
                    print(f"[INFO] Deleted project folder: {project_folder}")
                else:
                    print("[DEBUG] Project folder does not exist")

                self.ids.project_button.text = "Select Current Project"
                popup.dismiss()

            except PermissionError as e:
                print(f"[ERROR] Permission denied while deleting project: {e}")
            except Exception as e:
                print(f"[ERROR] Failed to delete project: {e}")

        # Show popup
        popup = Popup(title="Confirm Deletion", size_hint=(None, None), size=(400, 200))
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(Label(text=f"Are you sure you want to delete '{selected_project}'?"))
        btn_box = BoxLayout(size_hint_y=None, height=44, spacing=10)
        btn_box.add_widget(Button(text="Cancel", on_release=popup.dismiss))
        btn_box.add_widget(Button(text="Delete", on_release=confirm_deletion))
        box.add_widget(btn_box)
        popup.add_widget(box)
        popup.open()
        
        self.ids.delete_button.disabled = True
