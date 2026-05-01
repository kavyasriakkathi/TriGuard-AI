import sys
import csv
import os
from classifier import process_ticket
from responder import get_response
from logger import log_ticket
from pattern_detector import detect_incidents

from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn

console = Console()

def print_separator():
    console.rule()

def main():
    console.print("[bold cyan]TriGuard AI: Intelligent Incident Auto-Grouping & Routing Engine[/bold cyan]")
    console.rule()

    input_csv = "support_issue.csv" # Changed to match actual file in directory
    output_csv = "output.csv"

    if not os.path.exists(input_csv):
        console.print(f"[red]Error: Could not find {input_csv}. Please make sure it exists.[/red]")
        # Create dummy file if missing just to let the user see it work
        with open(input_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['ticket_id', 'user_query'])
            writer.writeheader()
            writer.writerow({'ticket_id': '1', 'user_query': 'My payment failed!'})
            writer.writerow({'ticket_id': '2', 'user_query': 'Payment declined but money deducted'})
            writer.writerow({'ticket_id': '3', 'user_query': 'I cannot login to my account'})
        console.print(f"[yellow]Created a sample {input_csv} file for testing.[/yellow]")

    with open(input_csv, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        if not reader.fieldnames or ('ticket_id' not in reader.fieldnames and 'user_query' not in reader.fieldnames):
            console.print(f"[red]Error: {input_csv} must have 'ticket_id' and 'user_query' headers.[/red]")
            return
        rows = list(reader)

    # Incident Auto-Grouping System
    console.print("[yellow]Running Smart Pattern Detection & Clustering...[/yellow]")
    incidents, standalone_ids = detect_incidents(rows)
    
    ticket_map = {row['ticket_id']: row for row in rows}
    
    processed_count = escalated_count = replied_count = 0

    with open(output_csv, "w", encoding="utf-8", newline='') as outfile:
        fieldnames = ['ticket_id', 'user_query', 'domain', 'issue_type', 'severity', 'priority_score', 'action', 'response']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None),
            TextColumn("{task.percentage:>3.0f}%"),
            TimeElapsedColumn()
        ) as progress:
            task = progress.add_task("Processing tickets & Incidents...", total=len(rows))
            
            # Process Incidents as Batches
            for incident_name, ticket_ids in incidents.items():
                volume = len(ticket_ids)
                representative_ticket = ticket_map[ticket_ids[0]]
                # Dynamic severity boosted by volume
                classification = process_ticket(representative_ticket['user_query'], volume_multiplier=volume)
                
                domain = classification["domain"]
                issue_type = classification["issue_type"]
                severity = classification["severity"]
                priority_score = classification["priority_score"]
                
                action = "ESCALATE TO INCIDENT RESPONSE" if priority_score >= 80 else "Automated Incident Reply"
                response = get_response(domain, issue_type, severity, is_incident=True)
                
                console.print(f"🚨 [bold red]DETECTED INCIDENT:[/bold red] {incident_name} ({volume} tickets affected) -> {domain} - {issue_type} [{severity}]")
                
                for tid in ticket_ids:
                    t_text = ticket_map[tid]['user_query']
                    log_ticket(tid, t_text, classification, response, is_incident=True)
                    writer.writerow({
                        'ticket_id': tid,
                        'user_query': t_text,
                        'domain': domain,
                        'issue_type': issue_type,
                        'severity': severity,
                        'priority_score': priority_score,
                        'action': action,
                        'response': response
                    })
                    processed_count += 1
                    if priority_score >= 80:
                        escalated_count += 1
                    else:
                        replied_count += 1
                    progress.advance(task)
                    
            # Process Standalone Tickets
            for tid in standalone_ids:
                t_text = ticket_map[tid]['user_query']
                classification = process_ticket(t_text, volume_multiplier=1)
                
                domain = classification["domain"]
                issue_type = classification["issue_type"]
                severity = classification["severity"]
                priority_score = classification["priority_score"]
                
                action = "ESCALATE TO HUMAN SUPPORT" if priority_score >= 80 else "Automated Reply"
                response = get_response(domain, issue_type, severity, is_incident=False)
                
                log_ticket(tid, t_text, classification, response, is_incident=False)
                writer.writerow({
                    'ticket_id': tid,
                    'user_query': t_text,
                    'domain': domain,
                    'issue_type': issue_type,
                    'severity': severity,
                    'priority_score': priority_score,
                    'action': action,
                    'response': response
                })
                
                processed_count += 1
                if priority_score >= 80:
                    escalated_count += 1
                    console.print(f"Ticket #{tid}: [Score: {priority_score}] [{severity}] [AUTO-ESCALATED]", style="red")
                else:
                    replied_count += 1
                    console.print(f"Ticket #{tid}: [Score: {priority_score}] [{severity}] [Auto-Replied]", style="green")
                progress.advance(task)

    print_separator()
    console.print("[bold]SYSTEM DASHBOARD SUMMARY[/bold]")
    console.rule()
    console.print(f"Total Tickets Processed : {processed_count}")
    console.print(f"Total Incidents Detected: {len(incidents)}")
    console.print(f"Human Escalations       : {escalated_count}")
    console.print(f"Automated Replies       : {replied_count}")
    console.print(f"Data Saved To           : {output_csv}")
    console.print(f"Audit Logs Appended     : logs.json")
    console.rule()
    console.print("Process Complete. System Standby.", style="magenta")
    console.rule()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\nExiting TriGuard AI. Have a great day!", style="magenta")
        sys.exit(0)