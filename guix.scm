(define-module (dalili)
  #:use-module (guix gexp)
  #:use-module (guix packages)
  #:use-module (guix download)
  #:use-module (guix git-download)
  #:use-module (guix build-system python)
  #:use-module (guix build-system pyproject)
  #:use-module (gnu packages)
  #:use-module (gnu packages check)
  #:use-module (gnu packages gcc)
  #:use-module (gnu packages python)
  #:use-module (gnu packages pkg-config)
  #:use-module (gnu packages python-crypto)
  #:use-module (gnu packages python-web)
  #:use-module (gnu packages python-xyz)
  #:use-module (gnu packages pdf)
  #:use-module (gnu packages swig)
  #:use-module (gnu packages ocr)
  #:use-module ((guix licenses) #:prefix license:))


(define %source-dir (dirname (current-filename)))

(package
  (name "dalili")
  (version "0.1")
  (source (local-file %source-dir "dalili-checkout"
		      #:recursive? #t
		      #:select? (git-predicate
				 %source-dir)))
  (build-system pyproject-build-system)
  (arguments `(#:tests? #f))
  (propagated-inputs (list python
			   python-minimal-wrapper
			   python-beautifulsoup4
			   python-certifi
			   python-charset-normalizer
			   python-idna
			   python-requests
			   python-soupsieve
			   python-urllib3
			   python-pytest
			   python-pdftotext))
  (home-page "https://github.com/nkabiru/dalili")
  (synopsis "A tool to notify you when Kenya Power has scheduled a power interruption in your area so that you can plan yourself accordingly.")
  (description "A tool to notify you when Kenya Power has scheduled a power interruption in your area so that you can plan yourself accordingly.")
  (license license:gpl3))
