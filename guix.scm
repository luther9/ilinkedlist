;;; This is the Guix package definition. It allows you to easily install this
;;; library from the source code using the Guix package manager. If you use
;;; Guix, type this command to install:
;;; guix package

(use-modules (guix build-system python)
	     (guix licenses))

(define-public python-ilinkedlist
  (package
   (name "python-ilinkedlist")
   (version "0.0.0")
   (source )
   (build-system python-build-system)
   (synopsis "An immutable linked-list library")
   (description
    "This is a Python implementation of immutable linked lists. It contains `nil` (the empty linked list) and a `Pair` class for nodes.")
   (home-page "https://github.com/luther9/ilinkedlist-py")
   (license gpl3+)))
