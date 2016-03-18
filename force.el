;;; force.el -- food ordering system
;;; Commentary:
;;; Code:
(setq force-project-name "force"
      force-project-dir "~/Documents/Stuff/force/"
      force-elconf-buffer (project-buffer-name-by-feature
                           force-project-name
                           "elconf")
      force-org-buffer (project-buffer-name-by-feature
                        force-project-name
                        "org")
      force-shell-buffer (project-buffer-name-by-feature
                          force-project-name
                          "shell")
      force-prodigy-buffer (project-buffer-name-by-feature
                            "prodigy"
                            force-project-name))

(defun buffer-exists (bufname)
  (not (eq nil (get-buffer bufname))))

(prodigy-define-service
  :name "Force"
  :command "~/.virtualenvs/force/bin/python"
  :args '("manage.py" "runserver")
  :init (lambda ()
          (defun force-menu-cleanup ()
            (interactive)
            (bpr-spawn "force cleanup"))
          (defun force-menu-fetch ()
            (interactive)
            (bpr-spawn "force fetch"))
          (defun force-push (cm)
            (interactive "MCommit message: ")
            (let* ((bpr-process-directory force-project-dir))
              (bpr-spawn (concatenate 'string "fab push:cm=\'" cm "\'"))))
          (defun force-deploy ()
            (interactive)
            (let* ((bpr-process-directory force-project-dir))
              (bpr-spawn "fab deploy")))
          (pyvenv-workon force-project-name)
          (if (not (buffer-exists force-shell-buffer))
              (spawn-shell force-shell-buffer force-project-dir))
          (if (not (buffer-exists force-elconf-buffer))
              (progn
                (find-file (concatenate 'string force-project-dir "/" force-project-name ".el"))
                (rename-buffer force-elconf-buffer)))
          (if (not (buffer-exists force-org-buffer))
              (progn
                (find-file (concatenate 'string force-project-dir "/" force-project-name ".org"))
                (rename-buffer force-org-buffer)))
          (switch-to-buffer force-prodigy-buffer))
  :cwd force-project-dir
  :url "http://localhost:8000/"
  :tags '(django react node)
  :stop-signal 'kill
  :kill-signal 'sigkill
  :port 8000
  ;; (spawn-shell (project-buffer-name-by-feature force-project-name "heroku") force-project-dir "heroku run bash --app sizo")
  :env '(("DATABASE_URL" "postgres://akatovda:qwadzv@localhost:5432/force")
         ("DEBUG" "1"))
  :kill-process-buffer-on-stop t)
(provide 'force)
;;; force.el ends here
