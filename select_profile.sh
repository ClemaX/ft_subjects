#!/usr/bin/env bash

UNAME=$(uname -s)

PROFILE_DIR_LINUX="$HOME/.mozilla/firefox"
PROFILE_DIR_DARWIN="$HOME/Library/Application Support/Firefox/Profiles"

profiles_linux()
{
	PROFILE_DIR="$PROFILE_DIR_LINUX"

	PROFILES=($(grep '^Path=.*$' "$PROFILE_DIR/profiles.ini" | cut -d'=' -f2))
}

profiles_darwin()
{
	PROFILE_DIR="$PROFILE_DIR_DARWIN"

	pushd "$PROFILE_DIR" >/dev/null
		PROFILES=($(find . -type d -mindepth 1 -maxdepth 1 | cut -d'/' -f2-))
	popd >/dev/null
}

case "$UNAME" in
	Linux*)		profiles_linux;;
	Darwin*)	profiles_darwin;;
	*)			echo "Unknown system: '$UNAME'!" >&2 && exit 1;;
esac

PS3='Select profile, or 0 to exit: '
select PROFILE in "${PROFILES[@]}"
do
	if [[ $REPLY == "0" ]]
	then
		exit 1
	elif [[ -z $PROFILE ]]
	then
		echo 'Invalid choice!' >&2
	elif ! [ -d "$PROFILE_DIR/$PROFILE" ]
	then
		echo 'Profile directory does not exist!' >&2
	else
		break
	fi
done

echo "$PROFILE_DIR/$PROFILE"
