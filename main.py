import sys
import csv
import os
from classifier import process_ticket
from responder import get_response
from logger import log_ticket
from pattern_detector import detect_incidents
from learning_memory import update_memory
from ml_model import train_model, get_model_info
from rca_engine import generate_rca

from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel

console = Console()

def print_separator():
    console.rule()

def run_feedback_loop():
    """
    AI Learning Behavior Layer — Feedback Loop
    Allows human agents to correct misclassifications so the AI learns for next time.
    """
    console.print("\n[bold yellow]🧠 AI FEEDBACK LOOP — Train the System[/bold yellow]")
    console.rule()
    console.print("Correct a past classification so the AI remembers it next time.")
    console.print("Type [bold]'skip'[/bold] to skip.\n")
    
    ticket_text = input("Enter the ticket text to correct: ").strip()
    if ticket_text.lower() == 'skip':
        return False
    
    domain = input("Correct Domain (e.g., Payments, Security, HackerRank, AI Tools, Performance): ").strip()
    issue_type = input("Correct Issue Type (e.g., Transaction Failed, Account Compromise): ").strip()
    severity = input("Correct Severity (SEV-1, SEV-2, SEV-3, SEV-4): ").strip().upper()
    
    if domain and issue_type and severity:
        update_memory(ticket_text, domain, issue_type, severity)
        console.print(f"\n[green]✅ Memory updated! The AI will now classify similar tickets as:[/green]")
        console.print(f"   Domain: {domain} | Issue: {issue_type} | Severity: {severity}")
        
        # Trigger auto-retraining with the new feedback
        console.print("[yellow]🔄 Auto-retraining ML model with new feedback...[/yellow]")
        log = train_model(force=True)
        if log:
            console.print(f"[green]✅ Model retrained! Total training samples: {log['training_samples']} (Seed: {log['seed_samples']}, Feedback: {log['feedback_samples']})[/green]")
        return True
    else:
        console.print("[red]Invalid input. Skipping feedback.[/red]")
        return False

def main():
    console.print(Panel.fit(
        "[bold cyan]🛡️ TriGuard AI: Intelligent Incident Auto-Grouping & Routing Engine[/bold cyan]\n"
        "[dim]Powered by TF-IDF + SVM Machine Learning[/dim]",
        border_style="cyan"
    ))

    # Step 2 & 3: Train/Load the ML Model
    console.print("[yellow]🤖 Initializing ML Classification Model...[/yellow]")
    training_log = train_model()
    model_info = get_model_info()
    if model_info:
        console.print(f"[green]✅ Model ready — {model_info['training_samples']} training samples ({model_info['seed_samples']} seed + {model_info['feedback_samples']} feedback)[/green]")
    else:
        console.print("[green]✅ Model trained and ready.[/green]")
    console.rule()

    input_csv = "support_issue.csv"
    output_csv = "output.csv"

    if not os.path.exists(input_csv):
        console.print(f"[red]Error: Could not find {input_csv}. Please make sure it exists.[/red]")
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

    # Step 5: Incident Auto-Grouping (Pattern Detection)
    console.print("[yellow]🔍 Running Smart Pattern Detection & Clustering...[/yellow]")
    incidents, standalone_ids = detect_incidents(rows)
    
    ticket_map = {row['ticket_id']: row for row in rows}
    
    processed_count = escalated_count = replied_count = 0

    with open(output_csv, "w", encoding="utf-8", newline='') as outfile:
        fieldnames = ['ticket_id', 'user_query', 'domain', 'issue_type', 'severity', 'priority_score', 'action', 'response', 'source']
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
                classification = process_ticket(representative_ticket['user_query'], volume_multiplier=volume)
                
                domain = classification["domain"]
                issue_type = classification["issue_type"]
                severity = classification["severity"]
                priority_score = classification["priority_score"]
                source = classification.get("source", "ml_model")
                
                action = "ESCALATE TO INCIDENT RESPONSE" if priority_score >= 80 else "Automated Incident Reply"
                response = get_response(domain, issue_type, severity, is_incident=True)
                
                console.print(f"🚨 [bold red]DETECTED INCIDENT:[/bold red] {incident_name} ({volume} tickets affected) -> {domain} - {issue_type} [{severity}] [source: {source}]")
                
                incident_tickets = [ticket_map[tid] for tid in ticket_ids]
                rca = generate_rca(incident_name, domain, incident_tickets)
                console.print(f"   [dim cyan]🔬 RCA Generated: {rca['probable_cause']}[/dim cyan]")
                
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
                        'response': response,
                        'source': source
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
                source = classification.get("source", "ml_model")
                
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
                    'response': response,
                    'source': source
                })
                
                processed_count += 1
                if priority_score >= 80:
                    escalated_count += 1
                    console.print(f"Ticket #{tid}: [Score: {priority_score}] [{severity}] [AUTO-ESCALATED] [source: {source}]", style="red")
                else:
                    replied_count += 1
                    console.print(f"Ticket #{tid}: [Score: {priority_score}] [{severity}] [Auto-Replied] [source: {source}]", style="green")
                progress.advance(task)

    # Dashboard Summary
    print_separator()
    console.print("[bold]SYSTEM DASHBOARD SUMMARY[/bold]")
    console.rule()
    
    summary_table = Table(show_header=False, box=None, padding=(0, 2))
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="white bold")
    summary_table.add_row("Total Tickets Processed", str(processed_count))
    summary_table.add_row("Total Incidents Detected", str(len(incidents)))
    summary_table.add_row("Human Escalations", str(escalated_count))
    summary_table.add_row("Automated Replies", str(replied_count))
    summary_table.add_row("ML Model Source", "TF-IDF + SVM (scikit-learn)")
    summary_table.add_row("Training Samples", str(model_info['training_samples']) if model_info else "N/A")
    summary_table.add_row("Data Saved To", output_csv)
    summary_table.add_row("Audit Logs Appended", "logs.json")
    console.print(summary_table)
    
    console.rule()
    console.print("Process Complete. System Standby.", style="magenta")
    console.rule()
    
    # Step 1 & 3: Feedback Loop + Auto Retraining
    run_feedback_loop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\nExiting TriGuard AI. Have a great day!", style="magenta")
        sys.exit(0)