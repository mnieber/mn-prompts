function findNextTabStop(el: any, isForward?: boolean) {
  var universe = document.querySelectorAll(
    'input, button, select, textarea, a[href]'
  );
  var list = Array.prototype.filter.call(universe, function (item) {
    return item.tabIndex >= '0';
  });
  var index = list.indexOf(el);
  return isForward ?? true
    ? list[index + 1] || list[0]
    : list[index - 1] || list[list.length - 1];
}

export function tabToNext(event: any, isForward?: boolean) {
  findNextTabStop(event.target, isForward).focus();
}
