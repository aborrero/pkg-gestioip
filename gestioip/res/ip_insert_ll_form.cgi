#!/usr/bin/perl -w -T

# Copyright (C) 2011 Marc Uebel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



use strict;
use DBI;
use lib '../modules';
use GestioIP;


my $gip = GestioIP -> new();
my $daten=<STDIN>;
my %daten=$gip->preparer($daten);

my $server_proto=$gip->get_server_proto();

my $lang = $daten{'lang'} || "";
my ($lang_vars,$vars_file)=$gip->get_lang("","$lang");
my $base_uri = $gip->get_base_uri();


my $client_id = $daten{'client_id'} || $gip->get_first_client_id();
$gip->CheckInput("$client_id",\%daten,"$$lang_vars{mal_signo_error_message}","$$lang_vars{insert_ll_message}","$vars_file");

my $align="align=\"right\"";
my $align1="";
my $ori="left";
my $rtl_helper="<font color=\"white\">x</font>";
if ( $vars_file =~ /vars_he$/ ) {
	$align="align=\"left\"";
	$align1="align=\"right\"";
	$ori="right";
}


my @values_clientes=$gip->get_ll_clients("$client_id");
my $anz_ll_clients=$gip->count_ll_clients("$client_id");
my @values_locations=$gip->get_loc_all("$client_id");


print "<p>\n";
print "<form name=\"insertvlan_form\" method=\"POST\" action=\"$server_proto://$base_uri/res/ip_insert_ll.cgi\"><br>\n";
print "<table border=\"0\" cellpadding=\"5\" cellspacing=\"2\">\n";

print "<tr><td $align>$$lang_vars{ll_client_message}</td><td $align1>";
my $j=0;
my $ll_client_id_form="";
if ( $anz_ll_clients > "1" ) {

	print "<select name=\"ll_client_id\" size=\"1\">";
	print "<option></option>\n";
	my $opt;
	foreach $opt(@values_clientes) {
		if ( $values_clientes[$j]->[0] == "-1" ) {
			$j++;
			next;
		}

		print "<option value=\"$values_clientes[$j]->[0]\">$values_clientes[$j]->[1]</option>";
		$j++;
	}
	print "</select></td></tr>\n";
} else {
	print "&nbsp;<font color=\"gray\"><i>$$lang_vars{no_ll_clients_message}</i></font>\n";
	$ll_client_id_form="<input type=\"hidden\" value=\"-1\" name=\"ll_client_id\">";
}


print "<tr><td $align>$$lang_vars{tipo_message}</td><td $align1><input name=\"type\" type=\"text\"  size=\"15\" maxlength=\"50\"></td></tr>\n";
print "<tr><td $align>$$lang_vars{service_message}</td><td $align1><input name=\"service\" type=\"text\"  size=\"15\" maxlength=\"50\"></td></tr>\n";
print "<tr><td $align>$$lang_vars{description_message}</td><td $align1><input name=\"description\" type=\"text\"  size=\"15\" maxlength=\"100\"></td></tr>\n";
print "<tr><td $align>$$lang_vars{phone_number_message}</td><td $align1><input name=\"phone_number\" type=\"text\"  size=\"15\" maxlength=\"30\"></td></tr>\n";
print "<tr><td $align>$$lang_vars{administrative_number_message}</td><td $align1><input name=\"ad_number\" type=\"text\"  size=\"15\" maxlength=\"50\"></td></tr>\n";

$j=0;
print "<tr><td $align>$$lang_vars{loc_message}</td><td $align1><select name=\"loc_id\" size=\"1\">";
print "<option></option>";
foreach (@values_locations) {
        if ( $values_locations[$j]->[0] eq "-1") {
                $j++;
                next;
        }
        print "<option value=\"$values_locations[$j]->[0]\">$values_locations[$j]->[1]</option>";
        $j++;
}

print "</td></tr>\n";
print "<tr><td $align>$$lang_vars{room_message}</td><td $align1><input name=\"room\" type=\"text\" size=\"15\" maxlength=\"100\"></td></tr>\n";
print "<tr><td $align>$$lang_vars{connected_device_message}</td><td $align1><input name=\"device\" type=\"text\"  size=\"15\" maxlength=\"100\"></td></tr>\n";
print "<tr><td $align>$$lang_vars{comentario_message}</td><td $align1><input name=\"comment\" type=\"text\" size=\"30\" maxlength=\"500\"></td></tr>\n";


print "</table>\n";

print "<p>\n";

print "<script type=\"text/javascript\">\n";
	print "document.insertvlan_form.vlan_num.focus();\n";
print "</script>\n";

print "<span style=\"float: $ori\"><br><p>$ll_client_id_form<input type=\"hidden\" value=\"$client_id\" name=\"client_id\"><input type=\"submit\" value=\"$$lang_vars{add_message}\" name=\"B2\" class=\"input_link_w_net\"></form></span><br><p>\n";

$gip->print_end("$client_id");
