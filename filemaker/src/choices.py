import json
from pprint import pprint
from typing import List, Tuple, Any


class Question:

    def __init__(self, label="", desc="", info="", boolean=False, default=None, parent=None, choices=None):
        self.label: str = label
        self.desc: str = desc
        self.info: str = info
        self.boolean: bool = boolean
        self.default: any = default if default is not None else (False if boolean else "")
        self.parents: List[Tuple[str, Any]] = [] if parent is None else parent
        self.choices: List[str] = [] if choices is None else choices
        self.answer: Any = default

    def __repr__(self) -> str:
        return f"Question{{label={self.label}, answer={self.answer}, choices={self.choices}}}"

    def to_dict(self):
        return {"type": "question",
                "label": self.label,
                "desc": self.desc,
                "info": self.info,
                "boolean": self.boolean,
                "default": self.default,
                "parents": self.parents,
                "choices": self.choices,
                "answer": self.answer,
                }

    def add_parent(self, *parents):
        for parent in parents:
            self.parents.append(parent)

    def add_choice(self, *choices):
        for choice in choices:
            self.choices.append(choice)


all_questions = [

    Question(label="login",
             desc="Login",
             info="ViaRezo OAuth Username",
             default="2018barf"
             ),
    Question(label="email_address",
             desc="Email Address",
             info="Email address of the user",
             default="nope@student.cs-campus.fr"
             ),
    Question(label="website_name",
             desc="Website Name",
             info="Desired domain name of your website",
             default="mysite"
             ),

    Question(label="template",
             desc="Template",
             info="Which template dou you want to base you on?",
             default="static",
             parent=None,
             choices=["static", "python", "php"],
             ),

    Question(label="exposed_ports",
             desc="Exposed ports",
             info="The ports used by the app which should communicate to the outside (comma separated)",
             default="",
             parent=[("template", "python"),
                     ("template", "php"),
                     ],
             ),
    Question(label="build_script",
             desc="Build Script",
             info="Script to be run once the source had been cloned (ex: npm run build)",
             default="",
             parent=[("template", "python"),
                     ("template", "php"),
                     ],
             ),
    Question(label="start_script",
             desc="Start Script",
             info="Script to be run to start the application (ex: python3 server.py)",
             default="",
             parent=[("template", "python"),
                     ("template", "php"),
                     ],
             ),
    Question(label="use_mysql",
             desc="Use MySQL",
             info="The app needs a MySQL server",
             boolean=True,
             default=False,
             parent=[("template", "python"),
                     ("template", "php"),
                     ],
             ),

    Question(label="mysql_db_name",
             desc="Database name",
             info="This will create a phpmyadmin server",
             default="",
             parent=[("use_mysql", True)],
             ),
    Question(label="mysql_db_user",
             desc="Database username",
             info="The user that will connect to the database",
             default="root",
             parent=[("use_mysql", True)],
             ),
    Question(label="mysql_db_user_password",
             desc="User password",
             info="User password to connect to the database",
             default="password",
             parent=[("use_mysql", True)],
             ),
    Question(label="mysql_db_root_password",
             desc="Root password",
             info="Root password to connect to the database",
             default="password",
             parent=[("use_mysql", True)],
             ),
    Question(label="mysql_use_phpmyadmin",
             desc="Use phpmyadmin",
             info="This will create a phpmyadmin server",
             boolean=True,
             default=False,
             parent=[("use_mysql", True)],
             ),

    Question(label="requirements_path",
             desc="Path to requirements.txt",
             info="Path to requirements.txt file for pip (empty if none)",
             default="",
             parent=[("template", "python")],
             ),

    Question(label="persistent_source_dir",
             desc="Persistent source directory",
             info="Only tick if the source files can dynamically change (ex: upload of files next to source code)",
             boolean=True,
             default=False,
             parent=[("template", "php")],
             ),

    Question(label="repository_type",
             desc="Repository Type",
             info="Public GitHub, Private GitLab,...",
             default="github_public",
             choices=["github_public", "github_private", "gitlab_public", "gitlab_private"],
             ),
    Question(label="repository_url",
             desc="Repository URL",
             info="URL to clone the project",
             default="",
             ),
    Question(label="root_folder",
             desc="Sources Root Directory",
             info="Root of your code (empty if directly at the root of the repository files)",
             default="",
             ),
]


all_questions_dict = [question.to_dict() for question in all_questions]
all_questions_json = json.dumps(all_questions_dict)


if __name__ == "__main__":
    # print(root_choice_json)
    pprint(all_questions_dict, width=180)
