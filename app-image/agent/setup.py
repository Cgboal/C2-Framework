from setuptools import setup

setup(name="C2F_Agent",
      version="0.1.3",
      description="The agent daemon component of the Command and Control framework",
      url="https://git.veldt.me/cgboal/C2-Framework",
      author="Calum Boal",
      author_email="cgboal@protonmail.com",
      license="MIT",
      packages=['agent', 'agent.db', 'agent.lib'],
      entry_points={
            "console_scripts": [
                'c2d = agent.__main__:main'
            ]
      },
      install_requires=[
          "docker",
          "urllib3",
          "python-crontab"
      ],

    )
