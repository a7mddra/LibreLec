class Config:
    # Browser Settings
    VIEWPORT = {'width': 1920, 'height': 1080}
    HEADLESS = False
    
    # Timeouts (ms)
    TIMEOUT_PAGE_LOAD = 5000
    TIMEOUT_CANVAS = 8000
    TIMEOUT_FRAME_SEARCH = 2000
    
    # Selectors
    SELECTOR_PAGE = "#viewer .page"
    SELECTOR_CANVAS = ".canvasWrapper canvas"
    SELECTOR_VIEWER_CONTAINER = "#viewerContainer"
    
    # DRM/Viewer Keywords
    VIEWER_KEYWORDS = ["pdfjs-drm", "viewer.html", "content/1/"]
    
    # Defaults
    DEFAULT_OUTPUT_FOLDER_NAME = "output_slides"
