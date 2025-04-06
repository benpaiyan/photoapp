import os
import configparser
import shutil
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
            size: root.size
            pos: root.pos
        Color:
            rgba: app.theme.main_background
        Rectangle:
            size: root.size
            pos: root.pos
            source: 'data/mainbg.png'

    BoxLayout:
        orientation: 'vertical'
    

        MainHeader:
            NormalButton:
                text: 'back'
                on_release: app.show_menu()
            HeaderLabel:
                text: "Project Manager"
                halign: 'center'
                valign: 'middle'
                size_hint_y: None
                height: dp(40)

        BoxLayout:
            size_hint: 1, 1
            pos_hint: {"center_x": 0.85, "center_y": 0.5}

            GridLayout:
                cols: 1
                padding: dp(20)
                spacing: dp(20)
                size_hint: None, None
                width: dp(500)
                height: dp(500)
                pos_hint: {"center_x": 0.5, "center_y": 0.5}

                BoxLayout:
                    orientation: 'vertical'
                    size_hint: 1, None
                    height: dp(100)
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
                        size_hint: 1, None
                        height: dp(40)

                        NormalInput:
                            id: new_project_name
                            multiline: False
                            disable_lines: True
                            hint_text: 'Project Name'
                            on_text: ok_button.disabled = root.project_name_exists(self.text)

                        NormalButton:
                            id: ok_button
                            text: 'Ok'
                            on_release: root.create_project_folder(new_project_name.text)
                            size_hint_y: None
                            height: dp(40)

                BoxLayout:
                    orientation: 'vertical'
                    size_hint: 1, None
                    height: dp(100)
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

                    GridLayout:
                        size_hint: 1, None
                        size_hint_y: None
                        height: dp(55)
                        cols: 1

                        MenuStarterButtonWide:
                            id: project_button
                            text: 'Select Current Project'
                            size_hint_y: None
                            height: dp(44)
                            on_release: root.open_project_dropdown(self)
                            
                BoxLayout:
                    orientation: 'vertical'
                    size_hint: 1, None
                    height: dp(100)
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
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: 1, None
                        height: dp(40)
                        WideButton:
                            id: launch_button
                            text: 'Launch Project'
                            on_release: root.launch_project()
                            size_hint_y: None
                            height: dp(40)
                BoxLayout:
                    orientation: 'vertical'
                    size_hint: 1, None
                    height: dp(100)
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
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: 1, None
                        height: dp(40)
                        WideButton:
                            id: launch_button
                            text: 'Delete Project'
                            on_release:root.delete_selected_project()
                            size_hint_y: None
                            height: dp(40)

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
        
    

    def delete_selected_project(self):
        app = App.get_running_app()
        selected_project = self.ids.project_button.text.strip()

        if not selected_project or selected_project in ["Default_project", "Select Current Project"]:
            print("[WARNING] No valid project selected to delete!")
            return

        def confirm_deletion(instance):
            selected_project = self.ids.project_button.text.strip()
            app = App.get_running_app()

            config_dir = app.get_project_config_directory()
            project_name = selected_project.lower()

            config_path = os.path.join(config_dir, f"{project_name}.ini")
            project_folder_path = os.path.join(config_dir, project_name)

            print(f"[DEBUG] Deleting .ini: {config_path}")
            print(f"[DEBUG] Deleting folder: {project_folder_path}")

            try:
                # 👉 Optional: try to close database or cleanup before delete
                if hasattr(app, 'close_database_connection'):
                    print("[DEBUG] Attempting to close database connection.")
                    app.close_database_connection()

                # Delete the config file
                if os.path.exists(config_path):
                    os.remove(config_path)
                    print(f"[INFO] Deleted project config: {config_path}")
                else:
                    print(f"[WARNING] Project config not found: {config_path}")

                # Delete the project folder
                if os.path.exists(project_folder_path):
                    shutil.rmtree(project_folder_path)
                    print(f"[INFO] Deleted project folder: {project_folder_path}")
                else:
                    print(f"[WARNING] Project folder not found: {project_folder_path}")

                self.ids.project_button.text = "Select Current Project"
                print("[INFO] Project deleted successfully.")

            except Exception as e:
                print(f"[ERROR] Failed to delete project: {e}")

        def cancel_deletion(instance):
            print("[INFO] Deletion cancelled.")
            popup.dismiss()

        # Confirmation popup
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(Label(text=f"Are you sure you want to delete project '{selected_project}'?"))

        btn_box = BoxLayout(size_hint_y=None, height=44, spacing=10)
        btn_yes = Button(text="Yes")
        btn_no = Button(text="No")
        btn_box.add_widget(btn_yes)
        btn_box.add_widget(btn_no)

        box.add_widget(btn_box)

        popup = Popup(title="Confirm Deletion", content=box, size_hint=(None, None), size=(400, 200))
        btn_yes.bind(on_release=confirm_deletion)
        btn_no.bind(on_release=cancel_deletion)
        popup.open()