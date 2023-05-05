# Maintainer: Taha H. Nouibat <devacom at protonmail dot com>

pkgname='mounzil-git'
pkgver=1.0.0
pkgrel=1
pkgdesc="Qt front-end for aria2 download manager (Github version)."
arch=('any')
url="https://devacom.github.io/"
license=('GPL3')
depends=('aria2' 'ffmpeg' 'libnotify' 'libpulse' 'pyside6' 'python-psutil' 'python-requests' 'python-setproctitle' 'qt6-svg' 'sound-theme-freedesktop' 'yt-dlp' )
makedepends=('git' 'python-setuptools')
optdepends=('adwaita-qt6: for using adwaita style in GTK based Desktops.')
provides=("${pkgname%-git}")
conflicts=("${pkgname%-git}")
source=("${pkgname%-git}::git+https://github.com/devacom/mounzil.git")
sha256sums=('SKIP')

pkgver() {
    cd ${pkgname%-git}
    git describe --tags --long | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}

build() {
    cd ${pkgname%-git}
    python setup.py build
}

package() {
    cd ${pkgname%-git}
    python setup.py install --root="$pkgdir" --optimize=1 --skip-build
}
# vim:set ts=4 sw=4:
