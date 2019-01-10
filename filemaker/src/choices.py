"""
Here are the questions that will be displayed to the user.
All variables found in the templates should be assigned to a question
"""

import json
# from pprint import pprint
from typing import List, Tuple, Any


class Question:
    """
    Represents a question that will be displayed to the user.
    If `boolean` id True, the answer should be `True` or `False` (~checkbox).
    If `parents` is not empty, the question wll only be displayed when one of the conditions is fulfilled
        Conditions are under the format [(question1, answer1), (question2, answer2)]. The question will be
        displayed only if the answer to `question1` is `answer1` or if the answer to `question2` is `answer2`.
    If `choices` is not empty, the only acceptable solutions are the ones that are listed.
    """

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
        return str(self.to_dict())

    def to_dict(self):
        """Standard dict that can be transformed into a JSON"""
        return {"label": self.label,
                "desc": self.desc,
                "info": self.info,
                "boolean": self.boolean,
                "default": self.default,
                "parents": self.parents,
                "choices": self.choices,
                "answer": self.answer,
                }


all_questions = [

    Question(label="login",
             desc="Login",
             info="ViaRezo OAuth Username",
             default="2018barf",
             ),
    Question(label="email_address",
             desc="Email Address",
             info="Email address of the user",
             default="nope@student.cs-campus.fr",
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

    Question(label="website_name",
             desc="Website Name",
             info="Desired domain name of your website",
             default="mysite",
             ),
    Question(label="use_https",
             desc="Use HTTPS",
             info="The website should use HTTPS (recommended, all resources should also be secure)",
             boolean=True,
             default=True,
             ),

    Question(label="template",
             desc="Template",
             info="Which template dou you want to base you on?",
             default="static",
             parent=None,
             choices=["static", "python", "php", "react"],
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
                     ("template", "react"),
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
             info="Name of the database used by the code",
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
    Question(label="add_to_pythonpath",
             desc="Add to PYTHONPATH",
             info="Directories to add to the PYTHONPATH (separated by `:`, empty if none)",
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

    Question(label="dependencies_files",
             desc="Dependencies files",
             info="Files to install dependencies (separated by `:`, empty if none, ex: package.json:yarn.lock)",
             default="",
             parent=[("template", "react")],
             ),

    Question(label="env_variables",
             desc="ENV variables",
             info="Variables to add to ENV (syntax: VAR1=foo VAR2=\"bar baz\")",
             default="",
             parent=[("template", "python"),
                     ("template", "php"),
                     ("template", "react"),
                     ],
             ),
]


all_questions_dict = [question.to_dict() for question in all_questions]
all_questions_json = json.dumps(all_questions_dict)


if __name__ == "__main__":
    print("\n".join(str(question) for question in all_questions))
    # pprint(all_questions_dict, width=180)
