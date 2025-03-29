from pydantic import BaseModel, HttpUrl


class IndustryIdentifier(BaseModel):
    """Industry standard identifiers for books, such as ISBN-10, ISBN-13, or ISSN."""

    type: str
    identifier: str


class ReadingModes(BaseModel):
    """Available reading modes for the volume."""

    text: bool
    image: bool


class PanelizationSummary(BaseModel):
    """Information about comic-specific content formatting."""

    containsEpubBubbles: bool
    containsImageBubbles: bool


class ImageLinks(BaseModel):
    """URLs to book cover images in different sizes."""

    smallThumbnail: HttpUrl
    thumbnail: HttpUrl


class VolumeInfo(BaseModel):
    """Detailed information about a book volume."""

    title: str
    subtitle: str | None = None
    authors: list[str] | None = None
    publisher: str | None = None
    publishedDate: str | None = None
    description: str | None = None
    industryIdentifiers: list[IndustryIdentifier] | None = None
    readingModes: ReadingModes
    pageCount: int | None = None
    printType: str
    categories: list[str] | None = None
    maturityRating: str
    allowAnonLogging: bool
    contentVersion: str
    panelizationSummary: PanelizationSummary | None = None
    imageLinks: ImageLinks | None = None
    language: str
    previewLink: HttpUrl
    infoLink: HttpUrl
    canonicalVolumeLink: HttpUrl


class ListPrice(BaseModel):
    """Price information for a volume."""

    amount: float
    currencyCode: str


class SaleInfo(BaseModel):
    """Sales-related information for the volume."""

    country: str
    saleability: str
    isEbook: bool
    listPrice: ListPrice | None = None
    retailPrice: ListPrice | None = None
    buyLink: HttpUrl | None = None


class Epub(BaseModel):
    """Information about EPUB or PDF availability and access."""

    isAvailable: bool
    acsTokenLink: HttpUrl | None = None


class AccessInfo(BaseModel):
    """Access and availability information for the volume."""

    country: str
    viewability: str
    embeddable: bool
    publicDomain: bool
    textToSpeechPermission: str
    epub: Epub
    pdf: Epub
    webReaderLink: HttpUrl
    accessViewStatus: str
    quoteSharingAllowed: bool


class Volume(BaseModel):
    """Complete volume information combining metadata, sales, and access details."""

    kind: str
    id: str
    etag: str
    selfLink: HttpUrl
    volumeInfo: VolumeInfo
    saleInfo: SaleInfo
    accessInfo: AccessInfo
    searchInfo: dict | None = None


class GoogleBooksResponse(BaseModel):
    """Response structure from the Google Books API containing search results."""

    kind: str
    totalItems: int
    items: list[Volume]
