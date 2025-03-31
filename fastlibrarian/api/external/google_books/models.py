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
    readingModes: ReadingModes | None = None
    pageCount: int | None = None
    printType: str | None = None
    categories: list[str] | None = None
    maturityRating: str | None = None
    allowAnonLogging: bool | None = None
    contentVersion: str | None = None
    panelizationSummary: PanelizationSummary | None = None
    imageLinks: ImageLinks | None = None
    language: str | None = None
    previewLink: HttpUrl | None = None
    infoLink: HttpUrl | None = None
    canonicalVolumeLink: HttpUrl | None = None


class ListPrice(BaseModel):
    """Price information for a volume."""

    amount: float | None = None
    currencyCode: str | None = None


class SaleInfo(BaseModel):
    """Sales-related information for the volume."""

    country: str | None = None
    saleability: str | None = None
    isEbook: bool | None = None
    listPrice: ListPrice | None = None
    retailPrice: ListPrice | None = None
    buyLink: HttpUrl | None = None


class Epub(BaseModel):
    """Information about EPUB or PDF availability and access."""

    isAvailable: bool | None = None
    acsTokenLink: HttpUrl | None = None


class AccessInfo(BaseModel):
    """Access and availability information for the volume."""

    country: str | None = None
    viewability: str | None = None
    embeddable: bool | None = None
    publicDomain: bool | None = None
    textToSpeechPermission: str | None = None
    epub: Epub | None = None
    pdf: Epub | None = None
    webReaderLink: HttpUrl | None = None
    accessViewStatus: str | None = None
    quoteSharingAllowed: bool | None = None


class Volume(BaseModel):
    """Complete volume information combining metadata, sales, and access details."""

    kind: str
    id: str
    etag: str
    selfLink: HttpUrl | None = None
    volumeInfo: VolumeInfo | None = None
    saleInfo: SaleInfo | None = None
    accessInfo: AccessInfo | None = None
    searchInfo: dict | None = None


class GoogleBooksResponse(BaseModel):
    """Response structure from the Google Books API containing search results."""

    kind: str | None = None
    totalItems: int
    items: list[Volume]
