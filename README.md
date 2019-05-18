# Workaround for NVDA frequently losing focus in Vs Code

This add-on implements a workaround for a [known issue in VS Code](https://github.com/Microsoft/vscode/issues/28316) that causes NVDA to frequently lose focus when switching back to Code. Previously, the only solution when this occured was to restart Code, which is an unacceptable productivity killer, given how frequently it occurs.

## Known Issues

* When first starting Vs Code, there is an invisible window that NVDA gains focus on which shouldn't receive focus. I'll try to prevent this in a future version. For now, just alt-tab out and back into Vs Code.
* Any changes in the report background progress bars setting won't take effect in Vs Code until Code or NVDA is restarted so that the App Module reloads.