import appModuleHandler
import config
from controlTypes import ROLE_UNKNOWN
import eventHandler
import IAccessibleHandler
from NVDAObjects.IAccessible import IAccessible

class AppModule(appModuleHandler.AppModule):
    def __init__(self, *args, **kwargs):
        super(AppModule, self).__init__(*args, **kwargs)
        self.CODE_WINDOW_CLASS = "Chrome_RenderWidgetHostHWND"
        
        # A bug in VS Code causes NVDA to ignore all events when the document is no longer a child of the foreground
        # Prevent these events from being filtered as a workaround. See https://github.com/Microsoft/vscode/issues/28316
        eventsToRequest = { v for k, v in IAccessibleHandler.winEventIDsToNVDAEventNames.items() }
        # NVDA normally ignores these events in EventHandler.shouldAcceptEvent to prevent flooding
        eventsToRequest.remove("reorder")
        eventsToRequest.remove("show")
        # TODO: account for changing this setting after app module initialization
        if not config.conf["presentation"]["progressBarUpdates"]["reportBackgroundProgressBars"]:
            eventsToRequest.remove("valueChange")
        
        for event in eventsToRequest:
            eventHandler.requestEvents(eventName=event, processId=self.processID, windowClassName=self.CODE_WINDOW_CLASS)
    
    def event_NVDAObject_init(self, obj):
        if obj.windowClassName == self.CODE_WINDOW_CLASS and isinstance(obj, IAccessible) and obj.IAccessibleChildID < 0 and obj.role == ROLE_UNKNOWN:
            # #5439: Focus seems to hit Chromium objects that die before we can fetch them.
            obj.shouldAllowIAccessibleFocusEvent = False