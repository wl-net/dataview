Dataview Portal Application
===========================

Extending the portal with your own applications
---

#### The portal menu system

The portal relies on DATAVIEW_APPS to determine which applications should be displayed in the menu. Only applications that the user has any level of permission are shown. Dataview will prevent the user from accessing your application if they are not provided any level of access to it. Enforcement of authorization beyond all/nothing is left up to the specific application to determine.