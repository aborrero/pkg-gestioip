#!/usr/bin/perl -w -T

use strict;
use DBI;
use lib './modules';
use GestioIP;


my $gip = GestioIP -> new();
my $daten=<STDIN>;
my %daten=$gip->preparer($daten);

my ($lang_vars,$vars_file,$entries_per_page)=$gip->get_lang();

my $client_id = $daten{'client_id'} || $gip->get_first_client_id();


$gip->CheckInput("$client_id",\%daten,"$$lang_vars{mal_signo_error_message}","$$lang_vars{clients_message}","$vars_file");

$gip->PrintClientTab("$client_id","$vars_file");

$gip->print_end("$client_id");

