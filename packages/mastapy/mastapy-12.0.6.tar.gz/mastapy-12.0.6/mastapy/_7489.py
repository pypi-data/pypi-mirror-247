﻿"""_7489.py

TaskProgress
"""


from typing import (
    List, Callable, Iterable, Optional
)

from mastapy._internal import constructor, conversion
from mastapy._internal.class_property import classproperty
from mastapy._internal.python_net import python_net_import
from mastapy import _7483

_ARRAY = python_net_import('System', 'Array')
_STRING = python_net_import('System', 'String')
_ACTION = python_net_import('System', 'Action')
_TASK_PROGRESS = python_net_import('SMT.MastaAPIUtility', 'TaskProgress')


__docformat__ = 'restructuredtext en'
__all__ = ('TaskProgress',)


class TaskProgress(_7483.MarshalByRefObjectPermanent):
    """TaskProgress

    This is a mastapy class.
    """

    TYPE = _TASK_PROGRESS

    def __init__(self, instance_to_wrap: 'TaskProgress.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def title(self) -> 'str':
        """str: 'Title' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Title

        if temp is None:
            return ''

        return temp

    @property
    def status(self) -> 'str':
        """str: 'Status' is the original name of this property."""

        temp = self.wrapped.Status

        if temp is None:
            return ''

        return temp

    @status.setter
    def status(self, value: 'str'):
        self.wrapped.Status = str(value) if value is not None else ''

    @property
    def number_of_items(self) -> 'int':
        """int: 'NumberOfItems' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfItems

        if temp is None:
            return 0

        return temp

    @property
    def show_progress(self) -> 'bool':
        """bool: 'ShowProgress' is the original name of this property."""

        temp = self.wrapped.ShowProgress

        if temp is None:
            return False

        return temp

    @show_progress.setter
    def show_progress(self, value: 'bool'):
        self.wrapped.ShowProgress = bool(value) if value is not None else False

    @property
    def show_completion_status(self) -> 'bool':
        """bool: 'ShowCompletionStatus' is the original name of this property."""

        temp = self.wrapped.ShowCompletionStatus

        if temp is None:
            return False

        return temp

    @show_completion_status.setter
    def show_completion_status(self, value: 'bool'):
        self.wrapped.ShowCompletionStatus = bool(value) if value is not None else False

    @property
    def can_cancel(self) -> 'bool':
        """bool: 'CanCancel' is the original name of this property."""

        temp = self.wrapped.CanCancel

        if temp is None:
            return False

        return temp

    @can_cancel.setter
    def can_cancel(self, value: 'bool'):
        self.wrapped.CanCancel = bool(value) if value is not None else False

    @property
    def additional_string_to_add_to_title(self) -> 'str':
        """str: 'AdditionalStringToAddToTitle' is the original name of this property."""

        temp = self.wrapped.AdditionalStringToAddToTitle

        if temp is None:
            return ''

        return temp

    @additional_string_to_add_to_title.setter
    def additional_string_to_add_to_title(self, value: 'str'):
        self.wrapped.AdditionalStringToAddToTitle = str(value) if value is not None else ''

    @property
    def is_progress_tree_cell_expanded(self) -> 'bool':
        """bool: 'IsProgressTreeCellExpanded' is the original name of this property."""

        temp = self.wrapped.IsProgressTreeCellExpanded

        if temp is None:
            return False

        return temp

    @is_progress_tree_cell_expanded.setter
    def is_progress_tree_cell_expanded(self, value: 'bool'):
        self.wrapped.IsProgressTreeCellExpanded = bool(value) if value is not None else False

    @property
    def parent(self) -> 'TaskProgress':
        """TaskProgress: 'Parent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Parent

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @classproperty
    def null_task_progress(cls) -> 'TaskProgress':
        """TaskProgress: 'NullTaskProgress' is the original name of this property."""

        temp = TaskProgress.TYPE.NullTaskProgress

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @classproperty
    def null(cls) -> 'TaskProgress':
        """TaskProgress: 'Null' is the original name of this property."""

        temp = TaskProgress.TYPE.Null

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def child_tasks(self) -> 'List[TaskProgress]':
        """List[TaskProgress]: 'ChildTasks' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ChildTasks

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def is_aborting(self) -> 'bool':
        """bool: 'IsAborting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IsAborting

        if temp is None:
            return False

        return temp

    @property
    def fraction_complete(self) -> 'float':
        """float: 'FractionComplete' is the original name of this property."""

        temp = self.wrapped.FractionComplete

        if temp is None:
            return 0.0

        return temp

    @fraction_complete.setter
    def fraction_complete(self, value: 'float'):
        self.wrapped.FractionComplete = float(value) if value is not None else 0.0

    @property
    def additional_status_string(self) -> 'str':
        """str: 'AdditionalStatusString' is the original name of this property."""

        temp = self.wrapped.AdditionalStatusString

        if temp is None:
            return ''

        return temp

    @additional_status_string.setter
    def additional_status_string(self, value: 'str'):
        self.wrapped.AdditionalStatusString = str(value) if value is not None else ''

    def add_progress_status_updated(self, value: 'Callable[[str], None]'):
        """ 'add_ProgressStatusUpdated' is the original name of this method.

        Args:
            value (Callable[[str], None])
        """

        self.wrapped.add_ProgressStatusUpdated(value)

    def remove_progress_status_updated(self, value: 'Callable[[str], None]'):
        """ 'remove_ProgressStatusUpdated' is the original name of this method.

        Args:
            value (Callable[[str], None])
        """

        self.wrapped.remove_ProgressStatusUpdated(value)

    def add_progress_incremented(self, value: 'Callable[[float], None]'):
        """ 'add_ProgressIncremented' is the original name of this method.

        Args:
            value (Callable[[float], None])
        """

        self.wrapped.add_ProgressIncremented(value)

    def remove_progress_incremented(self, value: 'Callable[[float], None]'):
        """ 'remove_ProgressIncremented' is the original name of this method.

        Args:
            value (Callable[[float], None])
        """

        self.wrapped.remove_ProgressIncremented(value)

    def abort(self):
        """ 'Abort' is the original name of this method."""

        self.wrapped.Abort()

    def continue_with_progress(self, status_update: 'str', perform_analysis: 'Callable[[TaskProgress], None]') -> 'TaskProgress':
        """ 'ContinueWith' is the original name of this method.

        Args:
            status_update (str)
            perform_analysis (Callable[[mastapy.TaskProgress], None])

        Returns:
            mastapy.TaskProgress
        """

        status_update = str(status_update)
        method_result = self.wrapped.ContinueWith.Overloads[_STRING, _ACTION[_TASK_PROGRESS]](status_update if status_update else '', perform_analysis)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def continue_with(self, status_update: 'str', perform_analysis: 'Callable[..., None]') -> 'TaskProgress':
        """ 'ContinueWith' is the original name of this method.

        Args:
            status_update (str)
            perform_analysis (Callable[..., None])

        Returns:
            mastapy.TaskProgress
        """

        status_update = str(status_update)
        method_result = self.wrapped.ContinueWith.Overloads[_STRING, _ACTION](status_update if status_update else '', perform_analysis)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def get_all_errors(self) -> 'Iterable[str]':
        """ 'GetAllErrors' is the original name of this method.

        Returns:
            Iterable[str]
        """

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllErrors(), str)

    def increment_progress(self, inc: Optional['int'] = 1):
        """ 'IncrementProgress' is the original name of this method.

        Args:
            inc (int, optional)
        """

        inc = int(inc)
        self.wrapped.IncrementProgress(inc if inc else 0)

    def update_status_with_increment(self, new_status: 'str'):
        """ 'UpdateStatusWithIncrement' is the original name of this method.

        Args:
            new_status (str)
        """

        new_status = str(new_status)
        self.wrapped.UpdateStatusWithIncrement(new_status if new_status else '')

    def add_error(self, error: 'str'):
        """ 'AddError' is the original name of this method.

        Args:
            error (str)
        """

        error = str(error)
        self.wrapped.AddError(error if error else '')

    def complete(self):
        """ 'Complete' is the original name of this method."""

        self.wrapped.Complete()

    def subdivide(self, number_of_items: 'int') -> 'TaskProgress':
        """ 'Subdivide' is the original name of this method.

        Args:
            number_of_items (int)

        Returns:
            mastapy.TaskProgress
        """

        number_of_items = int(number_of_items)
        method_result = self.wrapped.Subdivide(number_of_items if number_of_items else 0)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def create_new_task(self, title: 'str', number_of_items: 'int', show_progress: Optional['bool'] = True, show_eta: Optional['bool'] = False, manual_increment: Optional['bool'] = False) -> 'TaskProgress':
        """ 'CreateNewTask' is the original name of this method.

        Args:
            title (str)
            number_of_items (int)
            show_progress (bool, optional)
            show_eta (bool, optional)
            manual_increment (bool, optional)

        Returns:
            mastapy.TaskProgress
        """

        title = str(title)
        number_of_items = int(number_of_items)
        show_progress = bool(show_progress)
        show_eta = bool(show_eta)
        manual_increment = bool(manual_increment)
        method_result = self.wrapped.CreateNewTask(title if title else '', number_of_items if number_of_items else 0, show_progress if show_progress else False, show_eta if show_eta else False, manual_increment if manual_increment else False)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def dispose(self):
        """ 'Dispose' is the original name of this method."""

        self.wrapped.Dispose()

    def to_string(self) -> 'str':
        """ 'ToString' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.ToString()
        return method_result

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.dispose()
