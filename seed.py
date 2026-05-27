"""Initialize DB schema and seed sample data."""
from app import create_app
from app.extensions import db
from app.models import User, Record
from config import Config

SAMPLE_RECORDS = [
    {
        "title": "The Dark Side of the Moon",
        "artist": "Pink Floyd",
        "year": 1973,
        "genre": "Rock",
        "condition": "new",
        "price": 42.0,
        "stock": 5,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/3e/76/b0/3e76b0e3-762b-2286-a019-8afb19cee541/886445635829.jpg/1000x1000bb.jpg",
        "description": "Remastered 180g vinyl pressing."
    },
    {
        "title": "Kind of Blue",
        "artist": "Miles Davis",
        "year": 1959,
        "genre": "Jazz",
        "condition": "new",
        "price": 38.0,
        "stock": 4,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music/7f/9f/d6/mzi.vtnaewef.jpg/1000x1000bb.jpg",
        "description": "Legacy edition, gatefold sleeve."
    },
    {
        "title": "Abbey Road",
        "artist": "The Beatles",
        "year": 1969,
        "genre": "Rock",
        "condition": "used",
        "price": 35.0,
        "stock": 2,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/48/53/43/485343e3-dd6a-0034-faec-f4b6403f8108/13UMGIM63890.rgb.jpg/1000x1000bb.jpg",
        "description": "Original UK pressing, very good condition."
    },
    {
        "title": "Graduation",
        "artist": "Kanye West",
        "year": 2007,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 45.0,
        "stock": 8,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music128/v4/39/25/2d/39252d65-2d50-b991-0962-f7a98a761271/00602517483507.rgb.jpg/1000x1000bb.jpg",
        "description": "Standard black vinyl reissue."
    },
    {
        "title": "Rumours",
        "artist": "Fleetwood Mac",
        "year": 1977,
        "genre": "Rock",
        "condition": "new",
        "price": 36.0,
        "stock": 6,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/4d/13/ba/4d13bac3-d3d5-7581-2c74-034219eadf2b/081227970949.jpg/1000x1000bb.jpg",
        "description": "180g audiophile pressing."
    },
    {
        "title": "Thriller",
        "artist": "Michael Jackson",
        "year": 1982,
        "genre": "Pop",
        "condition": "new",
        "price": 39.0,
        "stock": 7,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/32/4f/fd/324ffda2-9e51-8f6a-0c2d-c6fd2b41ac55/074643811224.jpg/1000x1000bb.jpg",
        "description": "Reissue with original artwork."
    },
    {
        "title": "To Pimp a Butterfly",
        "artist": "Kendrick Lamar",
        "year": 2015,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 48.0,
        "stock": 5,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music112/v4/b5/a6/91/b5a69171-5232-3d5b-9c15-8963802f83dd/15UMGIM15814.rgb.jpg/1000x1000bb.jpg",
        "description": "Double LP."
    },
    {
        "title": "Blue Train",
        "artist": "John Coltrane",
        "year": 1958,
        "genre": "Jazz",
        "condition": "new",
        "price": 41.0,
        "stock": 4,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/6e/1a/13/6e1a134d-8f6f-d90f-b855-ea69436a2e8b/17UM1IM45370.rgb.jpg/1000x1000bb.jpg",
        "description": "Blue Note tone poet series."
    },
    {
        "title": "OK Computer",
        "artist": "Radiohead",
        "year": 1997,
        "genre": "Rock",
        "condition": "new",
        "price": 44.0,
        "stock": 6,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/07/60/ba/0760ba0f-148c-b18f-d0ff-169ee96f3af5/634904078164.png/1000x1000bb.jpg",
        "description": "OKNOTOK reissue."
    },
    {
        "title": "Random Access Memories",
        "artist": "Daft Punk",
        "year": 2013,
        "genre": "Electronic",
        "condition": "new",
        "price": 49.0,
        "stock": 5,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/86/b1/92/86b192cf-ceb6-6e51-9361-dc4a35e95d22/196589921154.jpg/1000x1000bb.jpg",
        "description": "Double LP."
    },
    {
        "title": "Back in Black",
        "artist": "AC/DC",
        "year": 1980,
        "genre": "Rock",
        "condition": "used",
        "price": 30.0,
        "stock": 3,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/1e/14/58/1e145814-281a-58e0-3ab1-145f5d1af421/886443673441.jpg/1000x1000bb.jpg",
        "description": "Used, near mint."
    },
    {
        "title": "MUSIC",
        "artist": "Playboi Carti",
        "year": 2025,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 50.0,
        "stock": 8,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/03/24/10/03241047-f22d-7e64-3932-6df7550acc42/25UMGIM46212.rgb.jpg/1000x1000bb.jpg",
        "description": "Triple LP, gatefold."
    },
    {
        "title": "Whole Lotta Red",
        "artist": "Playboi Carti",
        "year": 2020,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 47.0,
        "stock": 6,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/ba/1e/05/ba1e058e-5637-e53c-563c-f5b9a1a6c344/20UM1IM18331.rgb.jpg/1000x1000bb.jpg",
        "description": "Opium-era artwork, double LP."
    },
    {
        "title": "Donda",
        "artist": "Kanye West",
        "year": 2021,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 52.0,
        "stock": 5,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/62/13/7b/62137b3f-7722-59f5-2ee1-b5aff9426869/21UMGIM64738.rgb.jpg/1000x1000bb.jpg",
        "description": "Triple LP, black sleeve."
    },
    {
        "title": "Bully",
        "artist": "Kanye West",
        "year": 2024,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 55.0,
        "stock": 3,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/4b/38/d1/4b38d146-381d-ace2-73df-24074576e62b/656465138828_cover.jpg/1000x1000bb.jpg",
        "description": "Limited pressing."
    },
    {
        "title": "Punk",
        "artist": "Young Thug",
        "year": 2021,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 43.0,
        "stock": 4,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/79/4c/bf/794cbf06-2a6d-e396-632d-c850855ed3b3/075679765925.jpg/1000x1000bb.jpg",
        "description": "Double LP."
    },
    {
        "title": "thank u, next",
        "artist": "Ariana Grande",
        "year": 2019,
        "genre": "Pop",
        "condition": "new",
        "price": 38.0,
        "stock": 7,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/bb/69/07/bb6907de-8ad4-970b-3311-121320e1bf9c/19UMGIM03691.rgb.jpg/1000x1000bb.jpg",
        "description": "Standard black vinyl."
    },
    {
        "title": "brat",
        "artist": "Charli xcx",
        "year": 2024,
        "genre": "Electronic",
        "condition": "new",
        "price": 25.0,
        "stock": 10,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Video211/v4/78/ab/d9/78abd9a6-0d55-a50b-4910-5944f7202ade/Job0d6dc85f-9edc-476d-96cb-38349745a36b-209886601-PreviewImage_Preview_Image_Intermediate_nonvideo_sdr_329793320_1793175885-Time1764258659251.png/592x592bb.jpg",
        "description": "(Black Ice) Vinyl LP"
    },
    {
        "title": "So Much Fun",
        "artist": "Young Thug",
        "year": 2019,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 33.0,
        "stock": 1,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/1f/f3/57/1ff35761-4124-912a-baef-02b236c977df/075679838612.jpg/592x592bb.jpg",
        "description": "LP"
    },
    {
        "title": "REST IN BASS: ENCORE",
        "artist": "Che",
        "year": 2025,
        "genre": "Hip-Hop",
        "condition": "used",
        "price": 70.0,
        "stock": 15,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/d9/06/f9/d906f9b7-c2cc-ff7a-f2eb-c58b427c7473/810129965797.jpg/592x592bb.jpg",
        "description": "LP"
    },
    {
        "title": "Love Lasts Forever",
        "artist": "Destroy Lonely",
        "year": 2024,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 35.0,
        "stock": 1,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/fc/22/4d/fc224d64-5b2b-0d83-58e9-8081dd7a99dc/24UMGIM88179.rgb.jpg/1000x1000bb.jpg",
        "description": "LP"
    },
    {
        "title": "Jump Out",
        "artist": "OsamaSon",
        "year": 2025,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 47.0,
        "stock": 5,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/48/4d/4c/484d4cfe-903e-2277-857f-056fa40edb91/075679618436.jpg/592x592bf.jpg",
        "description": "LP"
    },
    {
        "title": "Vie",
        "artist": "Doja Cat",
        "year": 2025,
        "genre": "Pop",
        "condition": "new",
        "price": 50.0,
        "stock": 5,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Video211/v4/d6/e5/9e/d6e59eb2-faa8-befa-f3b0-e11d33b17e6e/Jobbd14d704-8480-4e42-8cee-915cd4173405-204695739-PreviewImage_Preview_Image_Intermediate_nonvideo_sdr_399984904_2361991478-Time1759256018824.png/592x592bb.jpg",
        "description": "LP"
    },
    {
        "title": "WE STILL DON'T TRUST YOU",
        "artist": "Future, Metro Boomin",
        "year": 2024,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 60.0,
        "stock": 10,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/48/55/f3/4855f346-fd74-fe8c-d75d-890b52213884/196871990844.jpg/592x592bb.jpg",
        "description": "LP"
    },
    {
        "title": "ICEMAN",
        "artist": "Drake",
        "year": 2026,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 65.0,
        "stock": 15,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/f1/b2/cd/f1b2cd28-6edc-4dde-61a6-ff5f5ef94cd7/26UMGIM63614.rgb.jpg/592x592bb.jpg",
        "description": "LP"
    },
    {
        "title": "FOR NOTHING",
        "artist": "Nine Vicious",
        "year": 2025,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 58.0,
        "stock": 18,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/c2/84/20/c28420e1-b389-36a8-433d-b6856d837565/12185.jpg/592x592bb.webp",
        "description": "LP"
    },
    {
        "title": "Eternal Atake 2",
        "artist": "Lil Uzi Vert",
        "year": 2024,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 57.0,
        "stock": 13,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/c2/2a/67/c22a670e-c5ab-a14a-ba2f-63a76aae7d76/075679636348.jpg/592x592bb.jpg",
        "description": "LP"
    },
    {
        "title": "MASA",
        "artist": "YoungBoy Never Broke Again",
        "year": 2025,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 30.0,
        "stock": 15,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/63/53/9a/63539a84-2e0d-717f-4ea8-8cd80bb71cf5/25UMGIM90753.rgb.jpg/592x592bb.jpg",
        "description": "LP"
    },
    {
        "title": "Eternal Atake",
        "artist": "Lil Uzi Vert",
        "year": 2020,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 55.0,
        "stock": 17,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/99/36/ec/9936ec13-b95f-c909-0985-ff10a3c6a39f/075679831934.jpg/1000x1000bb.jpg",
        "description": "LP"
    },
    {
        "title": "Pink Tape",
        "artist": "Lil Uzi Vert",
        "year": 2023,
        "genre": "Hip-Hop",
        "condition": "new",
        "price": 88.0,
        "stock": 18,
        "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/11/65/d9/1165d9a5-a14f-3ced-00ca-9bc2e24026f8/075679676672.jpg/1000x1000bb.jpg",
        "description": "LP"
    }
]


def run():
    app = create_app()
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(email=Config.ADMIN_EMAIL).first():
            admin = User(email=Config.ADMIN_EMAIL, name="Admin", is_admin=True)
            admin.set_password(Config.ADMIN_PASSWORD)
            db.session.add(admin)
            print(f"Created admin: {Config.ADMIN_EMAIL} / {Config.ADMIN_PASSWORD}")

        added = 0
        updated = 0
        for data in SAMPLE_RECORDS:
            existing = Record.query.filter_by(title=data["title"], artist=data["artist"]).first()
            if existing is None:
                db.session.add(Record(**data))
                added += 1
                continue
            # Refresh image_url if missing or pointing at an outdated source.
            current = existing.image_url or ""
            if data.get("image_url") and (not current or "upload.wikimedia.org" in current):
                existing.image_url = data["image_url"]
                updated += 1
        print(f"Added {added} new records, refreshed {updated} cover image(s)")

        db.session.commit()
        print("Done.")


if __name__ == "__main__":
    run()