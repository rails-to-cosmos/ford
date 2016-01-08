(defun force ()
  "initialize force development workflow"
  (interactive)
  (defvar force-server t)
  (defvar force-root-dir "/Volumes/Main/Users/akatovda/Documents/Stuff/force")
  (dz-defservice force-server "/Volumes/Main/Users/akatovda/Documents/Stuff/force/forcenv/bin/python"
                 :args ("manage.py" "runserver")
                 :cd force-root-dir)
  (elscreen-create)
  (force-server-start)
  (delete-other-windows)
  (spawn-shell "*force-shell*" force-root-dir)
  (delete-other-windows))

(provide 'force)
