from bsky_login import bsky_login
from datetime import datetime, timedelta


def get_liked_posts(c):
    params = {"actor": c.me.handle}
    liked = []

    print("Getting Liked Posts...")

    while True:
        fetched = c.app.bsky.feed.get_actor_likes(params)
        if not fetched.feed:
            break
        liked += fetched.feed
        if not fetched.cursor:
            break
        params["cursor"] = fetched.cursor

    return liked


def get_old_like(c, post, d):

    print(
        f'Looking for like for post from "@{post.post.author.handle}":\n'
        f"-\t\t{post.post.record.text}\n"
        f"({post.post.indexed_at})"
        f". . . . . .\n"
    )

    params = {"uri": post.post.uri, "cid": post.post.cid}

    while True:
        fetched = c.app.bsky.feed.get_likes(params)

        if not fetched.likes:
            break

        for like in fetched.likes:
            if like.actor.handle == c.me.handle:
                print("Found like for post.\n")
                print(
                    "============================================================",
                    end="\n\n",
                )

                if is_old_like(like.created_at, d):
                    return post.post.viewer.like

                return

        if not fetched.cursor:
            break

        params["cursor"] = fetched.cursor


def unlike(c, l_uri):
    print("Deleting like...")
    c.unlike(l_uri)
    print("Like Deleted.", end="\n\n")
    print(
        "============================================================",
        end="\n\n",
    )


def is_old_like(created_at, d):
    created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
    days_ago = datetime.utcnow() - timedelta(days=d)
    if created_at < days_ago:
        return True


def main():
    client = bsky_login()
    liked_posts = get_liked_posts(client)
    print(f"Total Liked Posts: {len(liked_posts)}")

    if not input("Delete old likes? (Y/N)\n").upper() == "Y":
        return

    days = int(input("Enter the number of days: (30/90/180/365/...)\n"))

    if (
        not input(
            f"CONFIRM: Delete likes older than {days} days? (Y/N)\n"
            f"WARNING: THIS CANNOT BE UNDONE\n"
        ).upper()
        == "Y"
    ):
        return

    for liked_post in liked_posts:
        if is_old_like(liked_post.post.indexed_at, days):
            like_uri = get_old_like(client, liked_post, days)
            unlike(client, like_uri) if like_uri else None

    remaining_liked_posts = get_liked_posts(client)
    print(f"Previous Total Liked Posts: {len(liked_posts)}")
    print(f"Total Remaining Likes: {len(remaining_liked_posts)}")


if __name__ == "__main__":
    main()
