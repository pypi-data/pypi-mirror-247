from __future__ import annotations

import contextlib
from typing import Any, TYPE_CHECKING
from ooodev.adapter.adapter_base import GenericArgs
from ooodev.events.args.listener_event_args import ListenerEventArgs
from ooodev.utils import gen_util as gUtil
from .action_listener import ActionListener

if TYPE_CHECKING:
    from ooodev.utils.type_var import EventArgsCallbackT, ListenerEventCallbackT


class ActionEvents:
    """
    Class for managing Action Events.

    This class is usually inherited by control classes that implement ``com.sun.star.awt.XActionListener``.
    """

    def __init__(
        self,
        trigger_args: GenericArgs | None = None,
        cb: ListenerEventCallbackT | None = None,
        listener: ActionListener | None = None,
        subscriber: Any = None,
    ) -> None:
        """
        Constructor

        Args:
            trigger_args (GenericArgs, optional): Args that are passed to events when they are triggered.
                This only applies if the listener is not passed.
            cb (ListenerEventCallbackT | None, optional): Callback that is invoked when an event is added or removed.
            listener (ActionListener | None, optional): Listener that is used to manage events.
            subscriber (Any, optional): An UNO object that has a ``addActionListener()`` Method.
                If passed in then this instance listener is automatically added to it.
                Valid objects are: Listbox, ComboBox, Button, HyperLink, FixedHyperlink,
                ImageButton or any other UNO object that has ``addActionListener()`` method.
        """
        self.__callback = cb
        if listener:
            self.__listener = listener
            if subscriber:
                # several object such as Listbox, Combobox, Button, etc. can add an ActionListener.
                # There is no common interface for this, so we have to try them all.
                with contextlib.suppress(AttributeError):
                    subscriber.addActionListener(self.__listener)
        else:
            self.__listener = ActionListener(trigger_args=trigger_args, subscriber=subscriber)
        self.__name = gUtil.Util.generate_random_string(10)

    # region Manage Events
    def add_event_action_performed(self, cb: EventArgsCallbackT) -> None:
        """
        Adds a listener for an event.

        Event is invoked when an action is performed.

        The callback ``EventArgs.event_data`` will contain a UNO ``com.sun.star.awt.ActionEvent`` struct.
        """
        if self.__callback:
            args = ListenerEventArgs(source=self.__name, trigger_name="actionPerformed")
            self.__callback(self, args)
            if args.remove_callback:
                self.__callback = None
        self.__listener.on("actionPerformed", cb)

    def add_event_action_events_disposing(self, cb: EventArgsCallbackT) -> None:
        """
        Adds a listener for an event.

        Event is invoked when the broadcaster is about to be disposed.

        The callback ``EventArgs.event_data`` will contain a UNO ``com.sun.star.lang.EventObject`` struct.
        """

        if self.__callback:
            args = ListenerEventArgs(source=self.__name, trigger_name="disposing")
            self.__callback(self, args)
            if args.remove_callback:
                self.__callback = None
        self.__listener.on("disposing", cb)

    def remove_event_action_performed(self, cb: EventArgsCallbackT) -> None:
        """
        Removes a listener for an event
        """
        if self.__callback:
            args = ListenerEventArgs(source=self.__name, trigger_name="actionPerformed", is_add=False)
            self.__callback(self, args)
            if args.remove_callback:
                self.__callback = None
        self.__listener.off("actionPerformed", cb)

    def remove_event_action_events_disposing(self, cb: EventArgsCallbackT) -> None:
        """
        Removes a listener for an event
        """
        if self.__callback:
            args = ListenerEventArgs(source=self.__name, trigger_name="disposing", is_add=False)
            self.__callback(self, args)
            if args.remove_callback:
                self.__callback = None
        self.__listener.off("disposing", cb)

    @property
    def events_listener_action(self) -> ActionListener:
        """
        Returns listener
        """
        return self.__listener

    # endregion Manage Events
