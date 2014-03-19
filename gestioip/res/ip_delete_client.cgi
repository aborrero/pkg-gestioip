#!/usr/bin/perl -w -T

use strict;
use DBI;
use lib '../modules';
use GestioIP;


my $gip = GestioIP -> new();
my $daten=<STDIN>;
my %daten=$gip->preparer($daten);

my ($lang_vars,$vars_file,$entries_per_page)=$gip->get_lang();
my $base_uri = $gip->get_base_uri();

my $client_id = $daten{'client_id'} || $gip->get_first_client_id();
my $id = $daten{'id'} || "";
my $client = $daten{'client_name'} || "";

$gip->CheckInput("1",\%daten,"$$lang_vars{mal_signo_error_message}","$$lang_vars{delete_client_message}","$vars_file");

$gip->print_error("$client_id","$$lang_vars{formato_malo_message} (1)") if ! $id;
$gip->print_error("$client_id","$$lang_vars{formato_malo_message} (2)") if ! $client;

my $count_clients=$gip->count_clients();
my $default_client_id=$gip->get_default_client_id("$client_id") || "1";

#$gip->print_error("$client_id","$$lang_vars{one_client_needed_message}") if $count_clients == 1;
$gip->print_error("$client_id","$$lang_vars{default_client_not_delete_message}") if $id == 1;

$gip->delete_client("$id");
$gip->update_default_client("1","1") if $id == $default_client_id;


my $audit_type="34";
my $audit_class="5";
my $update_type_audit="1";
my $event="$client";
$gip->insert_audit("$client_id","$audit_class","$audit_type","$event","$update_type_audit","$vars_file");

print "<p><b>$$lang_vars{client_deleted_message}: $client</b><p>\n";

$gip->PrintClientTab("$client_id","$vars_file");

$gip->print_end("$client_id");

