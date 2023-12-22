import warnings
warnings.warn("It is not recommended to import directly from zrcl3.lazy as this will tank performance.")
def _warn_package_name(error):
	package_name = str(error).split()[-1]
	warnings.warn(f"Package missing: {package_name}")

try:
	from zrcl3.desktop_automation import (
		capture_window, 
		find_word_coordinates, 
	)
except ImportError as e:
	_warn_package_name(e)
	capture_window = None
	find_word_coordinates = None

try:
	from zrcl3.dictionary import (
		merge_dicts, 
		merge_two_dict, 
	)
except ImportError as e:
	_warn_package_name(e)
	merge_dicts = None
	merge_two_dict = None

try:
	from zrcl3.expirable_property import (
		ExpireOnFileProperty, 
		TimelyCachedProperty, 
		time_sensitive_cache, 
	)
except ImportError as e:
	_warn_package_name(e)
	ExpireOnFileProperty = None
	TimelyCachedProperty = None
	time_sensitive_cache = None

try:
	from zrcl3.github_download import (
		download_github_repo_file, 
	)
except ImportError as e:
	_warn_package_name(e)
	download_github_repo_file = None

try:
	from zrcl3.image import (
		base64_to_image, 
		image_to_base64, 
	)
except ImportError as e:
	_warn_package_name(e)
	base64_to_image = None
	image_to_base64 = None

try:
	from zrcl3.io import (
		create_bkup, 
	)
except ImportError as e:
	_warn_package_name(e)
	create_bkup = None

try:
	from zrcl3.list_module import (
		get_imports, 
		get_imports_via_ast, 
	)
except ImportError as e:
	_warn_package_name(e)
	get_imports = None
	get_imports_via_ast = None

try:
	from zrcl3.misc import (
		stringify_list, 
		unpack_tuple, 
	)
except ImportError as e:
	_warn_package_name(e)
	stringify_list = None
	unpack_tuple = None

try:
	from zrcl3.orjson_io_fallback import (
		load_json, 
		save_json, 
	)
except ImportError as e:
	_warn_package_name(e)
	load_json = None
	save_json = None

try:
	from zrcl3.passcrack import (
		crack_password, 
	)
except ImportError as e:
	_warn_package_name(e)
	crack_password = None

try:
	from zrcl3.singleton import (
		SingletonMeta, 
	)
except ImportError as e:
	_warn_package_name(e)
	SingletonMeta = None

try:
	from zrcl3.string import (
		format_vars, 
		is_valid_regex, 
		match_pattern, 
		match_patterns, 
		pattern_type, 
		rreplace, 
		simple_glob_pattern, 
	)
except ImportError as e:
	_warn_package_name(e)
	format_vars = None
	is_valid_regex = None
	match_pattern = None
	match_patterns = None
	pattern_type = None
	rreplace = None
	simple_glob_pattern = None

try:
	from zrcl3.subprocess import (
		check_invalid_cmdlet, 
		is_program_installed, 
	)
except ImportError as e:
	_warn_package_name(e)
	check_invalid_cmdlet = None
	is_program_installed = None

try:
	from zrcl3.verify_file import (
		checksum_verify, 
		is_size_within_range, 
	)
except ImportError as e:
	_warn_package_name(e)
	checksum_verify = None
	is_size_within_range = None

try:
	from zrcl3.win_process import (
		get_pid_from_hwnd, 
	)
except ImportError as e:
	_warn_package_name(e)
	get_pid_from_hwnd = None

try:
	from zrcl3.auto_click.ctx import (
		AutoClickCtx, 
		AutoClickMarker, 
	)
except ImportError as e:
	_warn_package_name(e)
	AutoClickCtx = None
	AutoClickMarker = None

try:
	from zrcl3.auto_click.shell import (
		auto_click_shell, 
	)
except ImportError as e:
	_warn_package_name(e)
	auto_click_shell = None

try:
	from zrcl3.auto_click import (
		create_click_command, 
		create_click_file, 
		create_click_folder, 
		create_click_module, 
	)
except ImportError as e:
	_warn_package_name(e)
	create_click_command = None
	create_click_file = None
	create_click_folder = None
	create_click_module = None

try:
	from zrcl3.auto_save_dict.on_trigger import (
		OnChangeSaveDict, 
	)
except ImportError as e:
	_warn_package_name(e)
	OnChangeSaveDict = None

try:
	from zrcl3.auto_save_dict.threaded import (
		AutoSaveDict, 
	)
except ImportError as e:
	_warn_package_name(e)
	AutoSaveDict = None

try:
	from zrcl3.hackthon.caller import (
		get_caller_func, 
		get_caller_name, 
		get_caller_trace, 
		get_self_name, 
	)
except ImportError as e:
	_warn_package_name(e)
	get_caller_func = None
	get_caller_name = None
	get_caller_trace = None
	get_self_name = None

try:
	from zrcl3.hackthon import (
		DoNothing, 
		lambda_constructor, 
		typing_literal_generator, 
	)
except ImportError as e:
	_warn_package_name(e)
	DoNothing = None
	lambda_constructor = None
	typing_literal_generator = None

try:
	from zrcl3.init_generator.other_solution import (
		generate_init, 
		geninit_TryCatchErrNone, 
		geninit_TryCatchErrWarning, 
		geninit_combined, 
	)
except ImportError as e:
	_warn_package_name(e)
	generate_init = None
	geninit_TryCatchErrNone = None
	geninit_TryCatchErrWarning = None
	geninit_combined = None

try:
	from zrcl3.init_generator import (
		gather_init_vars, 
		generate_init as generate_init_2,
	)
except ImportError as e:
	_warn_package_name(e)
	gather_init_vars = None
	generate_init_2 = None

try:
	from zrcl3.mediawiki.parser import (
		MediaWikiRaw, 
		MediaWikiRawBlob, 
		MediaWikiRawData, 
		MediaWikiRawVar, 
	)
except ImportError as e:
	_warn_package_name(e)
	MediaWikiRaw = None
	MediaWikiRawBlob = None
	MediaWikiRawData = None
	MediaWikiRawVar = None

try:
	from zrcl3.mediawiki import (
		MediaWikiConfig, 
	)
except ImportError as e:
	_warn_package_name(e)
	MediaWikiConfig = None

