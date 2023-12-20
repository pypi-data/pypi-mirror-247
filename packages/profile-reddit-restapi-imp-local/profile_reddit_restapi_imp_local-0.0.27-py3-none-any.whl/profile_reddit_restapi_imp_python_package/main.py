from handler import RedditImporter


def main():
    reddit_importer = RedditImporter()
    reddit_importer.handle()


if __name__ == "__main__":
    main()
